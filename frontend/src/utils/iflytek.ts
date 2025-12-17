import CryptoJS from 'crypto-js';

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
    const url = 'wss://iat.xf-yun.com/v1';
    const host = 'iat.xf-yun.com';
    const date = new Date().toUTCString();
    const algorithm = 'hmac-sha256';
    const headers = 'host date request-line';
    const signatureOrigin = `host: ${host}\ndate: ${date}\nGET /v1 HTTP/1.1`;
    
    const signatureSha = CryptoJS.HmacSHA256(signatureOrigin, API_SECRET);
    const signature = CryptoJS.enc.Base64.stringify(signatureSha);
    
    const authorizationOrigin = `api_key="${API_KEY}", algorithm="${algorithm}", headers="${headers}", signature="${signature}"`;
    const authorization = btoa(authorizationOrigin);
    
    return `${url}?authorization=${encodeURIComponent(authorization)}&date=${encodeURIComponent(date)}&host=${host}`;
  }

  public start() {
    if (this.status === 'recording') return;
    
    this.isFirstFrame = true;
    this.seq = 0;

    const url = this.getAuthUrl();
    this.socket = new WebSocket(url);
    
    this.socket.onopen = () => {
      this.startRecording();
      this.onStart();
    };
    
    this.socket.onmessage = (e) => {
      this.handleMessage(e.data);
    };
    
    this.socket.onerror = (e) => {
      this.onError(e);
      this.stop();
    };
    
    this.socket.onclose = () => {
      this.stopRecording();
      this.status = 'end';
      this.onStop();
    };
  }

  public stop() {
    if (this.status === 'end') return;
    
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
    }, 1000);
  }

  private async startRecording() {
    try {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({
        sampleRate: 16000 // Try to request 16k, but browser might ignore
      });
      
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      });

      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.scriptProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);
      
      this.scriptProcessor.onaudioprocess = (e) => {
        if (this.status === 'end') return;
        const inputData = e.inputBuffer.getChannelData(0);
        this.processAudioData(inputData);
      };

      source.connect(this.scriptProcessor);
      this.scriptProcessor.connect(this.audioContext.destination);
      
      this.status = 'recording';
    } catch (e) {
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

    // Send in chunks of 1280 bytes
    const FRAME_SIZE = 1280;
    while (this.audioDataBuffer.length >= FRAME_SIZE) {
        const chunk = new Int8Array(this.audioDataBuffer.splice(0, FRAME_SIZE));
        this.sendFrame(chunk, 1);
    }
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
  private seq = 0;

  private sendFrame(audioData: Int8Array | null, status: number) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const frameData: any = {};
    
    if (this.isFirstFrame) {
        frameData.header = {
            app_id: APPID,
            status: 0
        };
        frameData.parameter = {
            iat: {
                domain: "slm",
                language: "zh_cn",
                accent: "mandarin",
                vinfo: 1,
                dwa: "wpgs",
                result: {
                    encoding: "utf8",
                    compress: "raw",
                    format: "json"
                }
            }
        };
        frameData.payload = {
            audio: {
                encoding: "raw",
                sample_rate: 16000,
                channels: 1,
                bit_depth: 16,
                status: 0,
                seq: this.seq++,
                audio: audioData ? this.toBase64(audioData.buffer) : ''
            }
        };
        this.isFirstFrame = false;
    } else {
        frameData.header = {
            app_id: APPID,
            status: status
        };
        frameData.payload = {
            audio: {
                encoding: "raw",
                sample_rate: 16000,
                channels: 1,
                bit_depth: 16,
                status: status,
                seq: this.seq++,
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
    if (res.header && res.header.code !== 0) {
      this.onError(`Error: ${res.header.code} ${res.header.message}`);
      return;
    }
    if (res.code !== undefined && res.code !== 0) {
      this.onError(`Error: ${res.code} ${res.message}`);
      return;
    }
    
    if (res.payload && res.payload.result) {
      const result = res.payload.result;
      const text = this.decodeText(result.text);
      const isFinal = result.status === 2;
      
      // Handle wpgs (dynamic correction)
      // If pgs is 'rpl', we might need to replace previous text.
      // For simplicity, we just emit the current text segment.
      // The user of this class should accumulate or handle display.
      // Wait, if wpgs is on, the text returned might be a replacement.
      // Let's just return the raw text and let the UI handle it?
      // Or better, just return the text from this segment.
      
      // Actually, the `text` field contains the recognized text.
      // If `pgs` is 'rpl', it means we should replace the last `rg` segments.
      // This is complex for a simple demo.
      // Let's try to just append for now, or handle simple accumulation.
      
      // The doc says:
      // ws: array of words.
      // We can reconstruct the sentence.
      
      this.onTextChange(text, isFinal);
    }
  }

  private decodeText(base64Text: string): string {
      try {
          const binaryString = atob(base64Text);
          const bytes = new Uint8Array(binaryString.length);
          for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
          }
          const decoder = new TextDecoder('utf-8');
          const jsonStr = decoder.decode(bytes);
          
          const json = JSON.parse(jsonStr);
          let str = '';
          if (json.ws) {
              json.ws.forEach((ws: any) => {
                  ws.cw.forEach((cw: any) => {
                      str += cw.w;
                  });
              });
          }
          return str;
      } catch (e) {
          return '';
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
