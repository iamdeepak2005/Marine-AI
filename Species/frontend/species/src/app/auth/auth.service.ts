// src/app/auth/auth.service.ts

import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'authToken'; // Define your token key

  // Store the auth token
  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  // Retrieve the auth token
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  // Remove the auth token
  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  // Check if the user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken(); // Check if token exists
  }
}
