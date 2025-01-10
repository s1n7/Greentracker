import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HttpClientModule],
  template: '<h1>{{ message }}</h1>',
})
export class AppComponent {
  message: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // API-Aufruf
    this.http.get<{ message: string }>('/api/test/').subscribe({
      next: (data) => {
        this.message = data.message;
      },
      error: (err) => {
        console.error('API-Aufruf fehlgeschlagen:', err);
      }
    });
  }
}
