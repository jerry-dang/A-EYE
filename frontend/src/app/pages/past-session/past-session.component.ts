import { Component } from '@angular/core';
import { ToolbarComponent } from '../../components/toolbar/toolbar.component';
import { LineGraphComponent } from '../../components/line-graph/line-graph.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ActivatedRoute } from '@angular/router';
import { SessionService } from '../../services/session.service';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-past-session',
  standalone: true,
  imports: [ToolbarComponent, LineGraphComponent, MatProgressSpinnerModule],
  templateUrl: './past-session.component.html',
  styleUrl: './past-session.component.scss',
})
export class PastSessionComponent {
  constructor(private route: ActivatedRoute, private sessionService: SessionService) {}

  sessionId: string = '';
  list: any[] = [];
  public chart: any;
  score: number = 0;

  ngOnInit() {
    Chart.register(...registerables);
    this.route.paramMap.subscribe((params) => {
      this.sessionId = params.get('sessionid') || '';
      
      this.sessionService.getSession(Number(this.sessionId)).subscribe((res) => {
        this.list = res.map((entry: any) => ({
          timeStamp: entry.timestamp,
          focus_level: Number(entry.focus_level),
        }));

        this.list.sort((a, b) => {
          return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
        });

        this.createChart();
      });
    });
  }


  createChart() {
    const x = this.list.map((element) => this.formatDate(new Date(element.timeStamp)));
    const y = this.list.map((element) => element.focus_level);

    this.chart = new Chart('MyChart', {
      type: 'line', //this denotes tha type of chart
      
      data: {
        // values on X-Axis
        labels: this.list.map((element) => element.timeStamp),
        datasets: [
          {
            data: this.list.map((element) => element.focus_level),
            backgroundColor: 'blue',
            label: "Focus"
          },
        ],
      },
      options: {
        scales: {
          y: {
            min: 0,
            max: 10
          }
        }
      }
    });
  }

  calculateAverage() {
    const y = this.list.map((element) => element.focus_level);
    const z = y.reduce((partialSum, a) => partialSum + a, 0) / y.length;
    return Math.round(z * 10) / 10;
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
