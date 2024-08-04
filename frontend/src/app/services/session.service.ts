import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { BehaviorSubject } from 'rxjs';

enum NoiseLevel {
  QUIET = 'quiet',
  MODERATE = 'medium',
  LOUD = 'loud',
}

interface res {
  session_id?: string;
}

const POLLING_INTERVAL = 2000; // submit img once every 2 seconds

@Injectable({
  providedIn: 'root',
})
export class SessionService {
  constructor(private apiService: ApiService) {}

  public isActive: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(
    false
  );
  public isPaused: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public location: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >(undefined);
  public startTime: BehaviorSubject<Date | undefined> = new BehaviorSubject<
    Date | undefined
  >(undefined);
  public endTime: BehaviorSubject<Date | undefined> = new BehaviorSubject<
    Date | undefined
  >(undefined);
  public noiseLevel: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >("quiet");
  public id: BehaviorSubject<string | undefined> = new BehaviorSubject<
    any | undefined
  >(undefined);
  public elapsedTime: BehaviorSubject<number> = new BehaviorSubject(0);

  setLocation(location: string) {
    this.location.next(location);
  }

  setStartTime(dateTime: Date) {
    this.startTime.next(dateTime);
  }

  setNoiseLevel(noise_level: string) {
    this.noiseLevel.next(noise_level);
  }

  startSession() {
    const startTime = new Date();
    this.startTimer();
    console.log({
      location: this.location.value,
      startTime: startTime,
      noise_level: this.noiseLevel.value,
    });
    this.apiService
      .post<string>('/start_session/', {
        location: this.location.value,
        // startTime: startTime,
        noise_level: this.noiseLevel.value,
      })
      .subscribe((res) => {
        console.log(res);

          this.isActive.next(true);
          this.id.next(res);
          this.startTime.next(startTime);

      });
  }

  pauseSession() {
    this.pauseTimer();
    this.isPaused.next(true);
  }

  resumeSession() {
    this.startTimer();
    this.isPaused.next(false);
  }

  stopSession() {
    this.isActive.next(false);
    this.pauseTimer();
    this.elapsedTime.next(0);
    this.apiService.post('/end_session/', { session_id: Number(this.id.value) }).subscribe();
    this.location.next(undefined);
    this.startTime.next(undefined);
  }

  postImage(image: string) {
    console.log(this.id.value);
    // image string is b64-encoded
    this.apiService
      .post('/save_image/', {
        base64_string: image,
        // timeStamp: this.startTime.value,
        // userId: 'lalala',
        session_id: this.id.value,
      })
      .subscribe((_) => {
        //
      });
  }

  timerInterval: any;
  startTimer() {
    if (this.timerInterval) {
      return;
    }
    this.timerInterval = setInterval(() => {
      this.elapsedTime.next(this.elapsedTime.value + 1);
    }, 1000);
  }

  pauseTimer() {
    clearInterval(this.timerInterval);
    this.timerInterval = null;
  }

  getSession(sessionId: number) {
    return this.apiService.get<any>(`/get_image_data/?session_id=${sessionId}`);
  }

  getSessionList() {
    return this.apiService.get<any>(`/start_session/`);
  }
}
