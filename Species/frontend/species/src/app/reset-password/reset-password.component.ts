import { Component } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [],
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.css'
})
export class ResetPasswordComponent {
  token: string = '';
  newPassword: string = '';

  constructor(private userService: UserService) {}

  resetPassword() {
    const data = { token: this.token, new_password: this.newPassword };
    this.userService.resetPassword(data).subscribe(
      response => {
        console.log('Password reset successful!', response);
      },
      error => {
        console.error('Password reset failed', error);
      }
    );
  }

}
