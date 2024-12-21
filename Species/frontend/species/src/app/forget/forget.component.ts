import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { FormsModule, NgForm } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { VerifyComponent } from '../verify/verify.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog'; // Import MatDialogModule
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forget',
  templateUrl: './forget.component.html',
  styleUrl: './forget.component.css',
  standalone: true,  // Mark it as a standalone component
  imports: [FormsModule,HttpClientModule,MatDialogModule ], 
})
export class ForgetComponent {
pass: any;
email: any;
  constructor(private userService: UserService,private router: Router,private http: HttpClient,private dialog: MatDialog,private snackBar: MatSnackBar) {}
  placeholder: string | undefined = "Send Reset Mail";
  isPassword:boolean=false
  onSubmit(form: NgForm) {
    if (form.valid) {

      const email = this.email;
      this.userService.requestPasswordReset({ email }).subscribe(
        response => {
          console.log('Reset link sent:', response);
          
          // Optionally handle the response further
          if (response) {
            this.isPassword=true
            this.placeholder = "Reset Password";

            const dialogRef = this.dialog.open(VerifyComponent, {
              width: '400px',
              data: { email }
            });
        
            dialogRef.afterClosed().subscribe(result => {
              // Check the result and execute the print logic if 'Yes' is selected
              if (result) {
                
              }else{
                this.placeholder = "Reset Password";
                this.isPassword=false
                this.snackBar.open('Error Occured', 'Close', {
                  duration: 3000,
                  horizontalPosition: 'center',
                  verticalPosition: 'bottom',
                });
              }
            });
          }
        },
        error => {
          console.error('Error sending reset link:', error);
          this.snackBar.open('Enter correct Email', 'Close', {
            duration: 3000,
            horizontalPosition: 'center',
            verticalPosition: 'bottom',
          });
        }
      );
          }
  }
  resetPassword(){
    this.userService.resetPasswordWithPin({
      email: this.email,
      new_password: this.pass
    }).subscribe((resp:any)=>{
      if(resp.status=='Password has been reset successfully'){
        this.router.navigate(['/login']);
      }
      console.log(resp)
    })

  }
}
