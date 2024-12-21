// src/app/signup/signup.component.ts
import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl:'./signup.component.css',
  standalone: true,  // Mark it as a standalone component
  imports: [FormsModule,HttpClientModule], 
})
export class SignupComponent {
  username: string = '';
  email: string = '';
  password: string = '';

  constructor(private userService: UserService) {}

  signup() {
    const user = { username: this.username, email: this.email, password: this.password };
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
