-- CreateTable
CREATE TABLE "Content" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "targetAudience" TEXT,
    "duration" INTEGER NOT NULL,
    "style" TEXT NOT NULL,
    "services" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "progress" REAL NOT NULL DEFAULT 0,
    "currentStep" TEXT,
    "generatedContent" TEXT,
    "generatedPicture" TEXT,
    "generatedVoice" TEXT,
    "generatedMusic" TEXT,
    "generatedVideo" TEXT
);
