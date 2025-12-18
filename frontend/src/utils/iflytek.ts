import CryptoJS from 'crypto-js';
import { logger } from './logger';

const APPID = '44b30254';
const API_SECRET = 'ZmU1YzRkZjViNDEwMjhjMGE2ODk2Nzdm';
const API_KEY = 'a441aaac2ad3acbd456d7a51368c7787';

export class IflytekClient {
  private socket: WebSocket | null = null;
  private audioContext: AudioContext | null = null;
  private scriptProcessor: ScriptProcessorNode | null = null;
  private mediaStream: MediaStream | null = null;
  private status: 'init' | 'recording' | 'end' = 'init';
  
  public onTextChange: (text: string, isFinal: boolean) => void = () => {};
  public onError: (error: any) => void = () => {};
  public onStart: () => void = () => {};
  public onStop: () => void = () => {};

  constructor() {}

  private getAuthUrl(): string {
    const url = 'wss://iat-api.xfyun.cn/v2/iat';
    const host = 'iat-api.xfyun.cn';
    const date = new Date().toUTCString();
    const algorithm = 'hmac-sha256';
    const headers = 'host date request-line';
    const signatureOrigin = `host: ${host}\ndate: ${date}\nGET /v2/iat HTTP/1.1`;
    
    const signatureSha = CryptoJS.HmacSHA256(signatureOrigin, API_SECRET);
    const signature = CryptoJS.enc.Base64.stringify(signatureSha);
    
    const authorizationOrigin = `api_key="${API_KEY}", algorithm="${algorithm}", headers="${headers}", signature="${signature}"`;
    const authorization = btoa(authorizationOrigin);
    
    return `${url}?authorization=${encodeURIComponent(authorization)}&date=${encodeURIComponent(date)}&host=${host}`;
  }

  private sendInterval: any = null;

  public start() {
    if (this.status === 'recording') return;
    
    logger.info('Starting ASR session');
    this.status = 'init';
    this.isFirstFrame = true;
    this.audioDataBuffer = [];
    this.resultTextTemp.clear();

    const url = this.getAuthUrl();
    logger.info('ASR Auth URL generated', { url: url.replace(API_KEY, '***') });
    
    this.socket = new WebSocket(url);
    
    this.socket.onopen = () => {
      logger.info('ASR WebSocket Connected');
      this.startRecording();
      this.startSendingLoop();
      this.onStart();
    };
    
    this.socket.onmessage = (e) => {
      // 忽略已经结束的会话的消息
      if (this.status === 'end') return;
      this.handleMessage(e.data);
    };
    
    this.socket.onerror = (e) => {
      logger.error('ASR WebSocket Error', e);
      if (this.status !== 'end') {
        this.onError(e);
      }
      this.stop();
    };
    
    this.socket.onclose = (e) => {
      logger.info('ASR WebSocket Closed', { code: e.code, reason: e.reason });
      this.stopRecording();
      this.stopSendingLoop();
      const wasRecording = this.status === 'recording';
      this.status = 'end';
      if (wasRecording) {
        this.onStop();
      }
    };
  }

  private startSendingLoop() {
      this.stopSendingLoop();
      // 每20ms发送一次，降低延迟
      this.sendInterval = setInterval(() => {
          this.checkAndSend();
      }, 20);
  }

  private stopSendingLoop() {
      if (this.sendInterval) {
          clearInterval(this.sendInterval);
          this.sendInterval = null;
      }
  }

  private checkAndSend() {
      const FRAME_SIZE = 1280;
      while (this.audioDataBuffer.length >= FRAME_SIZE) {
          const chunk = new Int8Array(this.audioDataBuffer.splice(0, FRAME_SIZE));
          this.sendFrame(chunk, 1);
      }
  }

  public stop() {
    if (this.status === 'end') return;
    this.status = 'end'; // 立即标记为结束，阻止更多数据发送
    
    // 停止发送循环
    this.stopSendingLoop();
    
    // Send remaining data
    if (this.audioDataBuffer.length > 0) {
        const chunk = new Int8Array(this.audioDataBuffer);
        this.sendFrame(chunk, 2); // Last frame
        this.audioDataBuffer = [];
    } else {
        // If no data left, just send empty last frame
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.sendFrame(null, 2);
        }
    }
    
    // Wait a bit for final result then close
    setTimeout(() => {
      if (this.socket) {
        this.socket.close();
      }
      this.stopRecording();
    }, 1500);
  }

  private async startRecording() {
    try {
      logger.info('Requesting microphone access');
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({
        sampleRate: 16000 // Try to request 16k, but browser might ignore
      });
      
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true  // 自动增益控制，提高音量
        }
      });

      logger.info('Microphone access granted', { 
          sampleRate: this.audioContext.sampleRate,
          tracks: this.mediaStream.getAudioTracks().length
      });

      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      // 使用更小的缓冲区以降低延迟 (512 samples @ 16k = 32ms)
      this.scriptProcessor = this.audioContext.createScriptProcessor(512, 1, 1);
      
      this.scriptProcessor.onaudioprocess = (e) => {
        if (this.status === 'end') return;
        const inputData = e.inputBuffer.getChannelData(0);
        this.processAudioData(inputData);
      };

      source.connect(this.scriptProcessor);
      this.scriptProcessor.connect(this.audioContext.destination);
      
      this.status = 'recording';
    } catch (e) {
      logger.error('Microphone access failed', e);
      this.onError(e);
    }
  }

  private stopRecording() {
    if (this.scriptProcessor) {
      this.scriptProcessor.disconnect();
      this.scriptProcessor = null;
    }
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
      this.mediaStream = null;
    }
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
    this.status = 'init';
  }

  private audioDataBuffer: number[] = [];

  private processAudioData(data: Float32Array) {
    // Resample to 16000Hz if necessary
    let outputData = data;
    if (this.audioContext && this.audioContext.sampleRate !== 16000) {
        outputData = this.transcode(data);
    }

    // Convert to Int16 and push to buffer
    for (let i = 0; i < outputData.length; i++) {
      let s = Math.max(-1, Math.min(1, outputData[i]!));
      s = s < 0 ? s * 0x8000 : s * 0x7FFF;
      // Little Endian split
      this.audioDataBuffer.push(s & 0xFF);
      this.audioDataBuffer.push((s >> 8) & 0xFF);
    }

    // Sending is now handled by checkAndSend loop
  }

  private transcode(audioData: Float32Array): Float32Array {
    const sampleRate = this.audioContext?.sampleRate || 48000;
    const targetSampleRate = 16000;
    
    if (sampleRate === targetSampleRate) {
      return audioData;
    }
    
    const compression = sampleRate / targetSampleRate;
    const length = Math.floor(audioData.length / compression);
    const result = new Float32Array(length);
    let index = 0;
    let j = 0;
    
    while (index < length) {
        const offset = Math.floor(j);
        const nextOffset = Math.ceil(j);
        const weight = j - offset;
        const val = audioData[offset]! * (1 - weight) + (audioData[nextOffset] || 0) * weight;
        result[index] = val;
        j += compression;
        index++;
    }
    
    return result;
  }

  private isFirstFrame = true;
  private resultTextTemp: Map<number, string> = new Map();

  private sendFrame(audioData: Int8Array | null, status: number) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    let frameData: any = {};
    
    if (this.isFirstFrame) {
        this.resultTextTemp.clear();
        frameData = {
            common: {
                app_id: APPID
            },
            business: {
                language: "zh_cn",
                domain: "iat",
                accent: "mandarin",
                dwa: "wpgs",      // 动态修正
                vad_eos: 5000,   // 5秒静音才结束（平衡响应速度和连续说话）
                nunum: 1,        // 数字转阿拉伯数字
                ptt: 1           // 添加标点
            },
            data: {
                status: 0,
                format: "audio/L16;rate=16000",
                encoding: "raw",
                audio: audioData ? this.toBase64(audioData.buffer) : ''
            }
        };
        logger.info('Sending first frame', { business: frameData.business });
        this.isFirstFrame = false;
    } else {
        frameData = {
            data: {
                status: status,
                format: "audio/L16;rate=16000",
                encoding: "raw",
                audio: audioData ? this.toBase64(audioData.buffer) : ''
            }
        };
    }

    this.socket.send(JSON.stringify(frameData));
  }

  private toBase64(buffer: ArrayBufferLike): string {
    let binary = '';
    const bytes = new Uint8Array(buffer as ArrayBuffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]!);
    }
    return window.btoa(binary);
  }

  private handleMessage(data: string) {
    const res = JSON.parse(data);
    
    if (res.code !== 0) {
      // 10165 是会话句柄失效，通常发生在会话结束后，可以忽略
      if (res.code === 10165) {
        logger.warn('ASR Session expired (10165)', res);
        return;
      }
      logger.error('ASR Error Response', res);
      this.onError(`Error: ${res.code} ${res.message}`);
      return;
    }
    
    if (res.data && res.data.result) {
      const result = res.data.result;
      let text = "";
      if (result.ws) {
        result.ws.forEach((ws: any) => {
            ws.cw.forEach((cw: any) => {
                text += cw.w;
            });
        });
      }
      
      // Handle wpgs logic
      const sn = result.sn;
      const pgs = result.pgs;
      const rg = result.rg; // [start, end]

      if (pgs === 'rpl') {
          // Replace range
          const [start, end] = rg;
          for (let i = start; i <= end; i++) {
              this.resultTextTemp.delete(i);
          }
      }
      
      this.resultTextTemp.set(sn, text);

      // Reconstruct full text
      let fullText = "";
      const sortedKeys = Array.from(this.resultTextTemp.keys()).sort((a, b) => a - b);
      for (const key of sortedKeys) {
          fullText += this.resultTextTemp.get(key);
      }

      // status 2 means end of speech
      const isFinal = res.data.status === 2;
      
      if (text) {
          logger.data('ASR Text Received', { text, fullText, pgs, sn, rg, isFinal });
      }
      
      this.onTextChange(fullText, isFinal);
    } else {
        logger.data('ASR Response (No Result)', res);
    }
  }
}

export class IflytekTTSClient {
  private socket: WebSocket | null = null;
  private audioContext: AudioContext | null = null;
  private nextStartTime = 0;
  
  public onStart: () => void = () => {};
  public onStop: () => void = () => {};
  public onError: (error: any) => void = () => {};

  constructor() {}

  private getAuthUrl(): string {
    const url = 'wss://tts-api.xfyun.cn/v2/tts';
    const host = 'tts-api.xfyun.cn';
    const date = new Date().toUTCString();
    const algorithm = 'hmac-sha256';
    const headers = 'host date request-line';
    const signatureOrigin = `host: ${host}\ndate: ${date}\nGET /v2/tts HTTP/1.1`;
    
    const signatureSha = CryptoJS.HmacSHA256(signatureOrigin, API_SECRET);
    const signature = CryptoJS.enc.Base64.stringify(signatureSha);
    
    const authorizationOrigin = `api_key="${API_KEY}", algorithm="${algorithm}", headers="${headers}", signature="${signature}"`;
    const authorization = btoa(authorizationOrigin);
    
    return `${url}?authorization=${encodeURIComponent(authorization)}&date=${encodeURIComponent(date)}&host=${host}`;
  }

  public async speak(text: string, vcn: string = 'xiaoyan') {
    this.stop();
    
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    if (this.audioContext.state === 'suspended') {
      await this.audioContext.resume();
    }
    
    this.nextStartTime = this.audioContext.currentTime;
    this.onStart();

    const url = this.getAuthUrl();
    this.socket = new WebSocket(url);
    
    this.socket.onopen = () => {
      this.sendRequest(text, vcn);
    };
    
    this.socket.onmessage = (e) => {
      this.handleMessage(e.data);
    };
    
    this.socket.onerror = (e) => {
      this.onError(e);
      this.stop();
    };
    
    this.socket.onclose = () => {
      // Wait for audio to finish playing?
      // The socket closes when transmission is done, but audio might still be playing.
      // We can check audioQueue or just let it play out.
      // But we should probably trigger onStop when audio finishes.
      // For now, let's trigger onStop when socket closes, but that might be too early.
      // Let's rely on audio scheduling.
    };
  }

  public stop() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    if (this.audioContext) {
      // Don't close context, just suspend or stop nodes?
      // Actually, we can just clear the queue and maybe close context if we want to save resources.
      // But reusing context is better.
      // To stop playing immediately:
      this.audioContext.suspend();
      this.audioContext = null; // Force recreate next time to clear scheduled nodes
    }
    this.onStop();
  }

  private sendRequest(text: string, vcn: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const frame = {
      common: {
        app_id: APPID
      },
      business: {
        aue: "raw",
        vcn: vcn,
        speed: 50,
        volume: 50,
        pitch: 50,
        tte: "UTF8"
      },
      data: {
        status: 2,
        text: btoa(unescape(encodeURIComponent(text))) // Base64 encode UTF8 text
      }
    };
    
    this.socket.send(JSON.stringify(frame));
  }

  private handleMessage(data: string) {
    const res = JSON.parse(data);
    if (res.code !== 0) {
      this.onError(`TTS Error: ${res.code} ${res.message}`);
      this.stop();
      return;
    }

    if (res.data) {
      const audio = res.data.audio;
      if (audio) {
        this.playAudio(audio);
      }
      if (res.data.status === 2) {
        this.socket?.close();
      }
    }
  }

  private playAudio(base64Audio: string) {
    if (!this.audioContext) return;

    const audioData = this.base64ToArrayBuffer(base64Audio);
    // Raw PCM 16k 16bit mono
    const float32Data = this.int16ToFloat32(audioData);
    const audioBuffer = this.audioContext.createBuffer(1, float32Data.length, 16000);
    audioBuffer.getChannelData(0).set(float32Data);

    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(this.audioContext.destination);
    
    // Schedule
    const startTime = Math.max(this.audioContext.currentTime, this.nextStartTime);
    source.start(startTime);
    this.nextStartTime = startTime + audioBuffer.duration;
    
    source.onended = () => {
        // Check if this was the last one? 
        // Hard to know exactly without tracking.
        // But if socket is closed and time > nextStartTime, we are done.
        if ((!this.socket || this.socket.readyState === WebSocket.CLOSED) && 
            this.audioContext && this.audioContext.currentTime >= this.nextStartTime - 0.1) {
            this.onStop();
        }
    };
  }

  private base64ToArrayBuffer(base64: string): ArrayBuffer {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  }

  private int16ToFloat32(buffer: ArrayBuffer): Float32Array {
    const int16 = new Int16Array(buffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
      float32[i] = int16[i]! / 32768.0;
    }
    return float32;
  }
}
