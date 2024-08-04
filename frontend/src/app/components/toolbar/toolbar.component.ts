import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [],
  templateUrl: './toolbar.component.html',
  styleUrl: './toolbar.component.scss',
})
export class ToolbarComponent {
  constructor(private router: Router) {}

  navigateToSessionPage() {
    this.router.navigate(['/session']);
  }

  goToHistory() {
    this.router.navigate(['/history']);
  }

  goHome() {
    this.router.navigate(['/']);
  }
}
