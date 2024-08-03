import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

interface res {
  session_id?: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {}
  private endpoint = 'http://localhost:3000';

  post<T>(url: string, body: any, headers?: HttpHeaders) {
    const options = { headers, withCredentials: true };
    return this.http.post<T>(this.endpoint + url, body, options);
  }

  get<T>(url: string, params?: HttpParams, headers?: HttpHeaders) {
    const options = { params, headers, withCredentials: true };
    return this.http.get<T>(this.endpoint + url, options);
  }

  put<T>(url: string, body: any) {
    return this.http.put<T>(url, body, { withCredentials: true });
  }

  delete<T>(url: string) {
    return this.http.delete<T>(url, { withCredentials: true });
  }
}
