import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-sessions-toolbar',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './sessions-toolbar.component.html',
  styleUrls: ['./sessions-toolbar.component.scss'],
})
export class SessionsToolbarComponent {}
