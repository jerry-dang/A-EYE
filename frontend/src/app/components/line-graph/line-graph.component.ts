import { Component, Input } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-line-graph',
  standalone: true,
  imports: [],
  templateUrl: './line-graph.component.html',
  styleUrl: './line-graph.component.scss',
})
export class LineGraphComponent {
  public chart: any;

  // ngOnInit(): void {
  //   Chart.register(...registerables);
  //   this.createChart();
  // }

  // createChart() {
  //   this.chart = new Chart('MyChart', {
  //     type: 'line', //this denotes tha type of chart

  //     data: {
  //       // values on X-Axis
  //       labels: this.data.map((element) => element.timeStamp),
  //       datasets: [
  //         {
  //           data: this.data.map((element) => element.focus_level),
  //           backgroundColor: 'blue',
  //         },
  //       ],
  //     },
  //   });
  // }
}
