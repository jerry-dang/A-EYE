import { Component, EventEmitter, Input, Output } from '@angular/core';
import { WebcamImage, WebcamModule } from 'ngx-webcam';
import { Observable, Subject } from 'rxjs';
import { CommonModule } from '@angular/common';
import { SessionsToolbarComponent } from '../../components/sessions-toolbar/sessions-toolbar.component';
import { MatSelectModule } from '@angular/material/select';
import { SessionService } from '../../services/session.service';

@Component({
  selector: 'app-session-page',
  standalone: true,
  imports: [
    WebcamModule,
    CommonModule,
    SessionsToolbarComponent,
    MatSelectModule,
  ],
  templateUrl: './session-page.component.html',
  styleUrl: './session-page.component.scss',
})
export class SessionPageComponent {
  constructor(private sessionService: SessionService) {}

  public webcamImage: WebcamImage | null = null;
  private trigger: Subject<void> = new Subject<void>();
  protected triggerObservable: Observable<void> = this.trigger.asObservable();

  @Output() capturedImage: EventEmitter<WebcamImage> | null = null;

  triggerSnapshot() {
    this.trigger.next();
  }

  public handleImage(webcamImage: WebcamImage): void {
    this.webcamImage = webcamImage;
    console.log('Captured image: ', this.webcamImage);
  }
}
