import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';
import { CommonModule } from '@angular/common';

import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  standalone: true,  // Mark it as a standalone component
  imports: [FormsModule,HttpClientModule,CommonModule,MatSnackBarModule], 

})
export class LoginComponent {
  email: string = '';
  password: string = '';
  isRegistering: boolean=false;
  username: string = '';
  emailR: string = '';
  passwordR: string = '';


  constructor(private userService: UserService,private router: Router,private authService: AuthService,private snackBar: MatSnackBar) {}
  setAuthToken(token: string) {
    localStorage.setItem('authToken', token); // Store token in local storage
  }
  isActive: boolean = false; // Track if the register form is active

  toggleActive() {
    this.isActive = !this.isActive; // Toggle the active state
  }
  login() {
    const user = { email: this.email, password: this.password };
    console.log(user)
    this.userService.login(user).subscribe(
      response => {
        console.log('Login successful!', response);
        if (response.status){
          this.authService.setToken(response.status); 
          console.log('if case')
          const name = this.email.split('@')[0];
          localStorage.setItem('name', name);
          this.router.navigate(['/main'])
        }
        else{
          this.snackBar.open('Enter Correct Password ', 'Close', {
            duration: 3000,  // Time in milliseconds before the Snackbar disappears
            horizontalPosition: 'center',
            verticalPosition: 'bottom',
          });

        }
      },
      error => {
        this.snackBar.open('Enter Correct Password', 'Close', {
          duration: 3000,  // Time in milliseconds before the Snackbar disappears
          horizontalPosition: 'center',
          verticalPosition: 'bottom',
          panelClass:['snackBar']
        });
          }
    );
  }

  isAuthenticated() {
    return this.authService.isAuthenticated(); // Check if authenticated
  }
  toggleRegister() {
    this.isRegistering = true; // Set to true to show the sign-up form
  }

  toggleLogin() {
    this.isRegistering = false; // Set to false to show the sign-in form
  }
  signup() {
    const user = { username: this.username, email: this.emailR, password: this.passwordR };
    this.userService.signup(user).subscribe(
      response => {
        console.log('Signup successful!', response);
      },
      error => {
        console.error('Signup failed', error);
      }
    );
  }
}