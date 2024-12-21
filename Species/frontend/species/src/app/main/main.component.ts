import { HttpClient } from '@angular/common/http';
import { Component, NgModule,PipeTransform  } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { OnInit, ViewChild, ElementRef, AfterViewInit, OnDestroy } from '@angular/core';
 
import { HttpClientModule } from '@angular/common/http';  // Import HttpClientModule
import { UserService } from '../user.service';
import { DomSanitizer,SafeHtml  } from '@angular/platform-browser';
import { Map, MapStyle, config } from '@maptiler/sdk';
import '@maptiler/sdk/dist/maptiler-sdk.css'
import { HeaderComponent } from "../header/header.component";
import { MatSnackBar } from '@angular/material/snack-bar';
@Component({
  selector: 'app-main',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule, HeaderComponent],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})



export class MainComponent implements OnInit, AfterViewInit, OnDestroy {
  value: any;
  constructor(private userService: UserService,private sanitizer: DomSanitizer,private snackBar: MatSnackBar){}
  questions: string[] = [];
  map: Map | undefined;
  notStart:boolean=true
  startQuestion:any

  @ViewChild('map')
  private mapContainer!: ElementRef<HTMLElement>;

  ngOnInit(): void {
    this.value = localStorage.getItem('name');
    console.log('The name is ',this.value);
    config.apiKey = 'xelNL0nYgR8P3giyy9oj';
    this.userService.getMarineQuestions().subscribe((resp:any)=>{
      console.log(resp)
      this.startQuestion=resp
    })
  }


  ngAfterViewInit() {
    const initialState = { lng: 139.753, lat: 35.6844, zoom: 14 };

    this.map = new Map({
      container: this.mapContainer.nativeElement,
      style: MapStyle.STREETS,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom
    });
  }

  ngOnDestroy() {
    this.map?.remove();
  }
  messages: { content: SafeHtml, type: string, imageUrl?: string }[] = [];  
  mapVisible = false; 
  load: boolean = false; // Use 'boolean' (lowercase)
  fileInputValue: File | null = null; 
  recentChats: string[] = [];  // Array to hold recent chat titles
  userInput: string = ''; // For user input
  imagePreviewUrl: string | ArrayBuffer | null = null; // For image preview
  sidebarOpen: boolean = true; // Sidebar toggle state
  isMic:boolean=false
  
  sendMessage() {
    if (this.load) {
        return; // If a request is already in progress, do nothing
    }

    // Check if there is an image to upload
    if (this.fileInputValue) {
        // Check if user input is not empty
        if (this.userInput.trim() !== '') {
           this.messages.push({ content: this.userInput, type: 'user' });
           this.load=true
            this.uploadImages(); // Call the upload function
            this.fileInputValue = null; // Reset file input here
            return; // Exit the function to prevent further execution
        }
    }

    // This part executes only if there's no image to upload
    if (this.userInput.trim() !== '') {
        this.fileInputValue=null
        this.imagePreviewUrl=null
        this.load = true; // Set loading state to true
        console.log('called sendMessage');

        // Push user input message to messages array
        this.messages.push({ content: this.userInput, type: 'user' });

        const data = this.userInput; // Get the user input
        this.userInput = ''; // Clear input
        this.autoResizeAfterSend()

        // Call the userService to ask the question
        this.userService.askQuestion(data).subscribe(
            (response: any) => {
                console.log('response', response);
                this.load = false; // Reset loading state
                const formattedResponse = this.formatResponse(response.answer);

                // Mock the bot response and add it to the messages
                this.mockBotResponse(formattedResponse);
                // this.mockBotResponse(response.answer);
                this.questions = response.question.questions || response.question;

                console.log('questions:', this.questions);
            },
            error => {
                console.error('Answer failed', error);
                this.load = false; // Reset loading state on error
                this.mockBotResponse('Sorry, I couldn\'t understand that.');
            }
        );
    }
}
  

autoResize(event: Event): void {
  const textarea = event.target as HTMLTextAreaElement;
  textarea.style.height = 'auto'; // Reset the height

  // Calculate the maximum height (for 6 rows)
  const lineHeight = 24; // Adjust this value based on your CSS
  const maxRows = 6;
  const maxHeight = lineHeight * maxRows;

  // Set height to scroll height but not exceeding max height
  textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
}
formatResponse(answer: string): string {
  try {
    // Convert JSON-like response into actual JSON
    const jsonResponse = JSON.parse(answer);

    // Format JSON as structured HTML for display
    return `
      <div><strong>Scientific Name:</strong> ${jsonResponse["Scientific Name"]}</div>
      <div><strong>Family:</strong> ${jsonResponse["Family"]}</div>
      <div><strong>Key Characteristics:</strong> ${jsonResponse["Key Characteristics"]}</div>
      <div><strong>Habitat:</strong> ${jsonResponse["Habitat"]}</div>
      <div><strong>Ecological Roles:</strong> ${jsonResponse["Ecological Roles"]}</div>
      <div><strong>Notable Behaviors:</strong> ${jsonResponse["Notable Behaviors"]}</div>
    `;
  } catch (e) {
    console.error('Failed to parse response as JSON', e);
    return answer; // Return the raw response in case of parsing failure
  }}

autoResizeAfterSend(): void {
  const textarea = document.querySelector('textarea[name="userInput"]') as HTMLTextAreaElement;
  if (textarea) {
    textarea.style.height = 'auto'; // Reset the height

    // Calculate the maximum height (for 6 rows)
    const lineHeight = 24; // Adjust this value based on your CSS
    const maxRows = 6;
    const maxHeight = lineHeight * maxRows;

    // Set height to scroll height but not exceeding max height
    textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
  }
}

handleFileInput(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
      const files = Array.from(input.files);
      files.forEach(file => {
          const reader = new FileReader();
          
          reader.onload = () => {
              this.imagePreviewUrl = reader.result as string;

              // Check if the image is already added to messages
              const isImageExist = this.messages.some(message => message.imageUrl === this.imagePreviewUrl);

              if (!isImageExist) {
                  // this.messages.push({
                  //     imageUrl: this.imagePreviewUrl,
                  //     content: '',
                  //     type: 'user'
                  // });
                  this.messages.push({
                    imageUrl: this.imagePreviewUrl,
                    content: '',
                    type: '',
                  })

              }
          };
          
          reader.readAsDataURL(file);  // Read the file as data URL
      });
  }
}

uploadImages() {
  const formData = new FormData();

  // Loop through all the messages to find images and text
  this.messages.forEach((message, index) => {
    if (message.content) {
      formData.append('text', this.userInput); // Attach the text content (if any)
    }

    if (message.imageUrl) {
      // Convert data URL to a file
      const imageFile = this.dataURLtoFile(message.imageUrl, `image_${index}.png`);
      formData.append('files', imageFile, imageFile.name); // Append the image file with a unique name
    }
  });

  // Send the form data to the server
  this.userService.uploadImageForClassification(formData).subscribe(
    (response: any) => {
      console.log('Server response:', response);

      // Add the server response to the messages
      if (response) {
        // this.messages.push({
        //   content: response.result.final_conclusion,
        //   type: 'bot',
        // });
        console.log('this need to be priinted ',response.final_conclusion)
        let j = 1;
        for (let i of response.individual_responses) {
          // Apply special styling to the "The Image X Shows" message
          this.mockBotResponse(`
            <div style="text-align: center; font-size: 24px; font-weight: bold;  padding: 20px;">
              **The Image ${j} Shows**
            </div>
          `);
          console.log(i);
          this.mockBotResponse(i);
          j++;
        }
        
        // Apply special styling to the "The Conclusion:" message
        this.mockBotResponse(`
          <div style="text-align: center; font-size: 24px; font-weight: bold;  padding: 20px;">
            **The Conclusion:**
          </div>
        `);
        
        // Regular message for the final conclusion
        this.mockBotResponse(response.final_conclusion);
        
      }
      this.load = false;
    },
    (error) => {
      this.load = false;
      console.error('Error uploading images:', error);

      this.messages.push({
        content: 'Sorry, there was an error processing your images.',
        type: 'bot'
      });
    }
  );
}

capitalizeFirstLetter(string: string): string {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

dataURLtoFile(dataUrl: string, filename: string): File {
  const arr = dataUrl.split(',');

  // Use a null check for .match()
  const mimeMatch = arr[0].match(/:(.*?);/);
  if (!mimeMatch) {
      throw new Error("Invalid data URL: mime type not found");
  }
  const mime = mimeMatch[1];

  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}


      
  
transform(value: string): string {
  if (!value) return value;

  // Replace new lines with <br> and bold markers with <strong>
  let formattedValue = value
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text
    .replace(/\n/g, '<br>'); // New lines

  return formattedValue;
}

startSpeechRecognition() {
  this.isMic=true
  const recognition = new (window as any).webkitSpeechRecognition(); // Use webkitSpeechRecognition for Chrome
  recognition.lang = 'en-US'; // Set language
  recognition.interimResults = false; // We want only final results
  recognition.maxAlternatives = 1; // Only the best alternative

  recognition.start(); // Start the recognition

  // Handle the result event
  recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript; // Get the transcript
    this.userInput += transcript + ' '; // Append it to the user input
  };

  // Handle the error event
  recognition.onerror = (event: any) => {
    console.error('Speech recognition error:', event.error);
  };

  // Handle the end event
  recognition.onend = () => {
    console.log('Speech recognition service has stopped.');
  };
  this.isMic=false
}


  // Simulate a bot response
private mockBotResponse(data: string) {
    console.log('modified data', data);
    
    // Sanitize the response
    const botResponse = this.sanitizer.bypassSecurityTrustHtml(this.transform(data));
    
    this.messages.push({ content: botResponse, type: 'bot' });
  }

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }
  onQuestionClick(question: string): void {
    console.log('Question clicked:', question);
    this.userInput=question
  }


}
