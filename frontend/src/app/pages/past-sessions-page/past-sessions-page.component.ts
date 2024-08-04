import { Component } from '@angular/core';
import { ToolbarComponent } from '../../components/toolbar/toolbar.component';
import { LineGraphComponent } from '../../components/line-graph/line-graph.component';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { SessionService } from '../../services/session.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-past-sessions-page',
  standalone: true,
  imports: [ToolbarComponent, LineGraphComponent, CommonModule, MatProgressSpinnerModule],
  templateUrl: './past-sessions-page.component.html',
  styleUrl: './past-sessions-page.component.scss',
})
export class PastSessionsPageComponent {
  constructor(private router: Router, private sessionService: SessionService) {}
  sessions: any[] = [];
  isLoaded: boolean = false;

  ngOnInit() {
    this.sessionService.getSessionList().subscribe((res) => {
      this.sessions = res;
      this.sessions.sort((a, b) => b.id - a.id);
      this.isLoaded = true;
    });
  }

  navigateHistory(id: string) {
    this.router.navigate(['/history/' + id]);
  }

  formatDate(now: string | Date) {
    // Format the date as YYYY-MM-DD
    now = new Date(now);
    const formattedDate = now.toISOString().split('T')[0];

    // Format the time as HH:MM
    const formattedTime = now.toTimeString().split(' ')[0].slice(0, 5);
    const formattedDateTime = `${formattedDate} ${formattedTime}`;

    return formattedDateTime;
  }
}
