import { Component } from '@angular/core';
import { ToolbarComponent } from '../../components/toolbar/toolbar.component';
import { LineGraphComponent } from '../../components/line-graph/line-graph.component';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-past-sessions-page',
  standalone: true,
  imports: [ToolbarComponent, LineGraphComponent, CommonModule],
  templateUrl: './past-sessions-page.component.html',
  styleUrl: './past-sessions-page.component.scss',
})
export class PastSessionsPageComponent {
  constructor(private router: Router) {}

  sessions: any[] = [
    { date: new Date(), id: '1' },
    { date: new Date(), id: '2' },
    { date: new Date(), id: '3' },
  ];

  ngOnInit() {}

  navigateHistory(id: string) {
    this.router.navigate(['/history/' + id]);
  }

  formatDate(now: Date) {
    // Format the date as YYYY-MM-DD
    const formattedDate = now.toISOString().split('T')[0];

    // Format the time as HH:MM
    const formattedTime = now.toTimeString().split(' ')[0].slice(0, 5);
    const formattedDateTime = `${formattedDate} ${formattedTime}`;

    return formattedDateTime;
  }
}
