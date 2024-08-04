import { Component } from '@angular/core';
import { ToolbarComponent } from '../../components/toolbar/toolbar.component';
import { SessionPageComponent } from '../session-page/session-page.component';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [ToolbarComponent, SessionPageComponent],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss',
})
export class LandingPageComponent {}
