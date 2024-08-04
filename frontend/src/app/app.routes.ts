import { Routes } from '@angular/router';
import { LandingPageComponent } from './pages/landing-page/landing-page.component';
import { SessionPageComponent } from './pages/session-page/session-page.component';
import { PastSessionsPageComponent } from './pages/past-sessions-page/past-sessions-page.component';
import { PastSessionComponent } from './pages/past-session/past-session.component';

export const routes: Routes = [
  { path: '', component: LandingPageComponent },
  { path: 'session', component: SessionPageComponent },
  { path: 'history', component: PastSessionsPageComponent },
  { path: 'history/:sessionid', component: PastSessionComponent },
];
