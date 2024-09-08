export interface GeneralOptions {
  style: string;
  description: string;
  sceneAmount: number;
  duration: number;
  tone: string;
  vocabulary: string;
  targetAudience: string;
  services: {
    generate_image: boolean;
    generate_voice: boolean;
    generate_music: boolean;
    generate_video: boolean;
  };
}

export interface ContentOptions {
  pacing: string;
  description: string;
}

export interface VisualPromptOptions {
  pictureDescription: string;
  style: string;
  imageDetails: string;
  shotDetails: string;
}

export interface Scene {
  type: 'OPENING' | 'MAIN' | 'CLOSING';
  description: string;
}

export interface VisualPrompt {
  type: 'OPENING' | 'MAIN' | 'CLOSING';
  sceneNumber: number;
  description: string;
}

export interface AudioPrompt {
  type: string;
  sceneNumber: number;
  description: string;
}

export interface MusicPrompt {
  description: string;
}

export interface GeneratedContent {
  video_title: string;
  description: string;
  main_scenes: {
    scene_description: string;
    visual_prompt: string;
  }[];
}

export interface ContentCreationRequest {
  videoSubject: string;
  generalOptions: GeneralOptions;
  contentOptions: ContentOptions;
  visualPromptOptions: VisualPromptOptions;
}

export interface ContentCreationResponse {
  id: number;
  title: string;
  videoSubject: string;
  status: string;
  progress: number;
  currentStep: string | null;
  generatedContent: string; // JSON string of GeneratedContent
  generalOptions: GeneralOptions;
  contentOptions: ContentOptions;
  visualPromptOptions: VisualPromptOptions;
  scenes: Scene[];
  visualPrompts: VisualPrompt[];
  audioPrompts: AudioPrompt[];
  musicPrompt: MusicPrompt;
  generatedPicture?: string;
  generatedVoice?: string;
  generatedMusic?: string;
  generatedVideo?: string;
  errorMessage?: string;
  createdAt: string;
  updatedAt: string;
}