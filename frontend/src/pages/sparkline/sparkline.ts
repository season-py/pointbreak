import { Component, Input, ElementRef } from '@angular/core';

import { Chart  } from 'chart.js';

@Component({
  selector: 'sparkline',
  template: `
    <div>
      <canvas></canvas>
    </div>
  `
})
export class SparklinePage {

  @Input() symbol: string;

  constructor(private el: ElementRef) {
  }

  ngAfterViewInit() {
    var canvas = this.el.nativeElement.querySelector('canvas');
    var ctx = canvas.getContext('2d');
    ctx.canvas.height = 20;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['', '', '', '', '', ''],
        datasets: [{
          data: [12, 19, 3, 5, 2, 3],
        }]
      },
      options: {
        scales: {
          yAxes: [{
            gridLines: {
              display: false
            },
            display: false
          }],
          xAxes: [{
            gridLines: {
              display: false
            },
            display: false
          }],
        },
        legend: {
          display: false
        },
        tooltips: {
          enabled: false
        }
      }
    });
  }

}
