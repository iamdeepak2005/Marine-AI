// src/app/app-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { ForgetComponent } from './forget/forget.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { MainComponent } from './main/main.component';
import { HomeComponent } from './home/home.component';
import { AuthGuard } from './auth/auth.guard';

export const routes: Routes = [
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  {path:'forget',component:ForgetComponent},
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {path:'main',loadComponent: () => import('./main/main.component').then((c) => c.MainComponent),canActivate:[AuthGuard]},
  {path:'home',component:HomeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
