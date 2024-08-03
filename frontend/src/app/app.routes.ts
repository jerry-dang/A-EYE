import { Routes } from '@angular/router';
import { LandingPageComponent } from './pages/landing-page/landing-page.component';
import { SessionPageComponent } from './pages/session-page/session-page.component';

export const routes: Routes = [
  { path: '', component: LandingPageComponent },
  { path: 'session', component: SessionPageComponent },
];
