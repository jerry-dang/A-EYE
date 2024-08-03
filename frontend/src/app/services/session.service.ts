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
  public location: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >(undefined);
  public startTime: BehaviorSubject<Date | undefined> = new BehaviorSubject<
    Date | undefined
  >(undefined);
  public endTime: BehaviorSubject<Date | undefined> = new BehaviorSubject<
    Date | undefined
  >(undefined);
  public noiseLevel: BehaviorSubject<NoiseLevel | undefined> =
    new BehaviorSubject<NoiseLevel | undefined>(undefined);
  public id: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >(undefined);

  setLocation(location: string) {
    this.location.next(location);
  }

  setStartTime(dateTime: Date) {
    this.startTime.next(dateTime);
  }

  setNoiseLevel(noiseLevel: NoiseLevel) {
    this.noiseLevel.next(noiseLevel);
  }

  startSession() {
    this.apiService
      .post<res>('/start_session', {
        location: this.location.value,
        startTime: this.startTime.value,
        noiseLevel: this.noiseLevel.value,
      })
      .subscribe((res) => {
        if (res.session_id) {
          this.isActive.next(true);
          this.id.next(res.session_id!);
        }
      });
  }

  postImage(image: string) {
    // image string is b64-encoded
    this.apiService
      .post('/save_image', {
        image: image,
        timeStamp: new Date(),
        userId: 'lalala',
        sessionId: this.id.value,
      })
      .subscribe();
  }
}
