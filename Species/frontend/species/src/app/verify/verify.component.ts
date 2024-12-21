import { Component, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { UserService } from '../user.service';

@Component({
  selector: 'app-verify',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './verify.component.html',
  styleUrl: './verify.component.css'
})
export class VerifyComponent {
  email: any;
  constructor(public dialogRef: MatDialogRef<VerifyComponent>,@Inject(MAT_DIALOG_DATA) public data: { email: string },private userService: UserService){
    this.email = data.email;
    console.log('Email',this.email)
  }
  firstNO:any
  secondNO:any
  thirdNO:any
  fourthNO:any
  message:any
  onNoClick(): void {
    this.dialogRef.close(false); // Close with false on No
  }
  reset(){
    this.firstNO=''
    this.secondNO=''
    this.thirdNO=''
    this.fourthNO=''


  }
  verify(){
    const a=`${this.firstNO}${this.secondNO}${this.thirdNO}${this.fourthNO}`
    this.userService.verifyPin(this.email, a).subscribe(
      (resp: any) => {
        console.log(resp);
        if (resp.status === 'PIN verified successfully') {
          console.log('yaa brooo shi hain');
          this.dialogRef.close(true);
        } else {
          this.reset();
          this.message = 'Pin is wrong';
        }
      },
      (error) => {
        // Handle different error responses
        if (error.status === 400) {
          this.reset();
          this.message = 'Pin is wrong'; // Specific message for 400 error
        } else if (error.status === 500) {
          this.reset();
          this.message = 'System error, please try again later'; // Message for 500 error
        } else {
          this.reset();
          this.message = 'An unexpected error occurred. Please try again later.'; // General error message
        }
      }
    );
    
    

  }


}
