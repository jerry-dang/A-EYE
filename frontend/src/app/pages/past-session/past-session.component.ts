import { Component } from '@angular/core';
import { ToolbarComponent } from '../../components/toolbar/toolbar.component';
import { LineGraphComponent } from '../../components/line-graph/line-graph.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-past-session',
  standalone: true,
  imports: [ToolbarComponent, LineGraphComponent, MatProgressSpinnerModule],
  templateUrl: './past-session.component.html',
  styleUrl: './past-session.component.scss',
})
export class PastSessionComponent {
  constructor(private route: ActivatedRoute) {}

  sessionId: string = '';

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.sessionId = params.get('sessionid') || '';
      // get session
    });
  }
}
