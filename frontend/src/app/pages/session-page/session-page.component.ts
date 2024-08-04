import { Component, EventEmitter, Input, Output } from '@angular/core';
import { WebcamImage, WebcamModule } from 'ngx-webcam';
import { Observable, Subject, TimeInterval } from 'rxjs';
import { CommonModule } from '@angular/common';
import { SessionsToolbarComponent } from '../../components/sessions-toolbar/sessions-toolbar.component';
import { SessionService } from '../../services/session.service';
import { DropdownModule } from 'primeng/dropdown';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-session-page',
  standalone: true,
  imports: [
    WebcamModule,
    CommonModule,
    SessionsToolbarComponent,
    DropdownModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
  ],
  templateUrl: './session-page.component.html',
  styleUrl: './session-page.component.scss',
})
export class SessionPageComponent {
  public webcamImage: WebcamImage | null = null;
  private trigger: Subject<void> = new Subject<void>();
  protected triggerObservable: Observable<void> = this.trigger.asObservable();
  @Output() capturedImage: EventEmitter<WebcamImage> | null = null;

  constructor(protected sessionService: SessionService) {}

  timerInterval: any = null; // interval for polling image capture
  POLLING_INTERVAL = 2000; // snapshot poll every 2 seconds

  noiseLevels = ['quiet', 'moderate', 'loud'];
  control = new FormControl('');
  location = '';
  onLocationChange(newLocation: string): void {
    this.sessionService.setLocation(newLocation);
  }
  selectedNoiseLevel = 'quiet';
  onNoiseLevelChange(newNoiseLevel: string) {
    this.sessionService.setNoiseLevel(newNoiseLevel);
  }

  ngOnInit() {
    this.sessionService.isActive.subscribe((isActive) => {
      console.log(isActive);
      if (isActive) {
        if (this.timerInterval) {return;}
        this.timerInterval = setInterval((_: any) => {
          if (!this.sessionService.isPaused.value) {
            this.triggerSnapshot();
          }
        }, 2000);
      } else {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    });
  }

  triggerSnapshot() {
    this.trigger.next();
  }

  handleImage(webcamImage: WebcamImage): void {
    this.webcamImage = webcamImage;
    this.sessionService.postImage(webcamImage.imageAsBase64);
  }

  formatTime(seconds: number) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(
      2,
      '0'
    )}:${String(secs).padStart(2, '0')}`;
  }
}
