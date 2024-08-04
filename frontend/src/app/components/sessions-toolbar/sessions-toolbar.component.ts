import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { SessionService } from '../../services/session.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sessions-toolbar',
  standalone: true,
  imports: [MatIconModule, CommonModule],
  templateUrl: './sessions-toolbar.component.html',
  styleUrls: ['./sessions-toolbar.component.scss'],
})
export class SessionsToolbarComponent {
  constructor(
    private router: Router,
    protected sessionService: SessionService
  ) {}

  goHome() {
    this.router.navigate(['/']);
  }

  startSession() {
    this.sessionService.startSession();
    this.sessionService.isActive.next(true);
  }

  pauseSession() {
    this.sessionService.pauseSession();
    this.sessionService.isActive.next(false);
  }

  stopSession() {
    this.sessionService.stopSession();
  }
}
