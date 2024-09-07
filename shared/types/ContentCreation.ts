export interface GeneralOptions {
    style: string;
    description: string;
    sceneAmount: number;
    duration: number;
    tone: string;
    vocabulary: string;
    targetAudience: string;
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
    title: string;
    description: string;
    scenes: Scene[];
    visualPrompts: VisualPrompt[];
    audioPrompts: AudioPrompt[];
    musicPrompt: MusicPrompt;
  }
  
  export interface ContentCreationRequest {
    title: string;
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
    generatedContent: GeneratedContent;
    generalOptions: GeneralOptions;
    contentOptions: ContentOptions;
    visualPromptOptions: VisualPromptOptions;
    scenes: Scene[];
    visualPrompts: VisualPrompt[];
    audioPrompts: AudioPrompt[];
    musicPrompt: MusicPrompt;
    createdAt: string;
    updatedAt: string;
  }