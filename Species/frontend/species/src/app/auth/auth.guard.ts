// src/app/auth/auth.guard.ts

import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from './auth.service'; // Ensure the path is correct

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    // Check if the user is authenticated
    if (this.authService.isAuthenticated()) {
      return true; // Allow access if authenticated
    }

    // Redirect to the login page if not authenticated
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false; // Deny access
  }
}
