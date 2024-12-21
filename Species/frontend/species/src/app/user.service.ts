// src/app/user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';

interface SignupModel {
  username: string;
  email: string;
  password: string;
}

interface LoginModel {
  email: string;
  password: string;
}

interface ResetPasswordModel {
  token: string;
  new_password: string;
}
export interface resetPassword{
  email:string
}
interface BotResponse {
  answer: string;
}
// Create an interface for the response structure
export interface AskQuestionResponse {
  answer: string; // The answer provided by the AI
  question: {
    questions: string[]; // Array of questions related to the answer
  };
}
export interface VerifyPinResponse {
  status: string; // Expected response from the backend
}
export interface ResetPasswordRequest {
  email: string;
  new_password: string;
}




@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = 'http://localhost:8000'; // Change to HTTP for local development

  constructor(private http: HttpClient) {}

  signup(user: SignupModel): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup`, user);
  }

  login(user: LoginModel): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, user);
  }

  requestPasswordReset(data: resetPassword): Observable<any> {
    return this.http.post(`${this.apiUrl}/request-password-reset`, data);
  }

  resetPassword(data: ResetPasswordModel): Observable<any> {
    return this.http.post(`${this.apiUrl}/reset-password`, data);
  }
  askQuestion(data: string) {
    return this.http.post<AskQuestionResponse>(`${this.apiUrl}/ask-question/`, { user_question: data });
  }
  uploadImageForClassification(formData): Observable<any> {
    console.log(formData)

    return this.http.post<any>(`${this.apiUrl}/image`, formData);
}

verifyPin(email: string, pin: string): Observable<VerifyPinResponse> {
  // Send email and pin as a JSON object
  return this.http.post<VerifyPinResponse>(`${this.apiUrl}/verify-pin`, { email, pin });
}
  resetPasswordWithPin(data: ResetPasswordRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/reset-password-with-pin`, data);
  }
  getMarineQuestions(): Observable<string[]> {
    return this.http.get<any>(`${this.apiUrl}/suggestStart`).pipe(
      map(response => response.answer.slice(0, 4)) // Extract the top 4 questions
    );
  }
  
  

}
