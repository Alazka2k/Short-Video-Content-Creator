/*
  Warnings:

  - You are about to drop the column `description` on the `Content` table. All the data in the column will be lost.
  - You are about to drop the column `duration` on the `Content` table. All the data in the column will be lost.
  - You are about to drop the column `services` on the `Content` table. All the data in the column will be lost.
  - You are about to drop the column `style` on the `Content` table. All the data in the column will be lost.
  - You are about to drop the column `targetAudience` on the `Content` table. All the data in the column will be lost.
  - Added the required column `updatedAt` to the `Content` table without a default value. This is not possible if the table is not empty.
  - Added the required column `videoSubject` to the `Content` table without a default value. This is not possible if the table is not empty.

*/
-- CreateTable
CREATE TABLE "GeneralOptions" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "style" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "sceneAmount" INTEGER NOT NULL,
    "duration" INTEGER NOT NULL,
    "tone" TEXT NOT NULL,
    "vocabulary" TEXT NOT NULL,
    "targetAudience" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "GeneralOptions_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "ContentOptions" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "pacing" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "ContentOptions_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "VisualPromptOptions" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "pictureDescription" TEXT NOT NULL,
    "style" TEXT NOT NULL,
    "imageDetails" TEXT NOT NULL,
    "shotDetails" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "VisualPromptOptions_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Scene" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "type" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "Scene_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AudioPrompt" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "type" TEXT NOT NULL,
    "sceneNumber" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "AudioPrompt_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "VisualPrompt" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "type" TEXT NOT NULL,
    "sceneNumber" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "VisualPrompt_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "MusicPrompt" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "description" TEXT NOT NULL,
    "contentId" INTEGER NOT NULL,
    CONSTRAINT "MusicPrompt_contentId_fkey" FOREIGN KEY ("contentId") REFERENCES "Content" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Content" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "videoSubject" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "progress" REAL NOT NULL DEFAULT 0,
    "currentStep" TEXT,
    "generatedContent" TEXT,
    "generatedPicture" TEXT,
    "generatedVoice" TEXT,
    "generatedMusic" TEXT,
    "generatedVideo" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);
INSERT INTO "new_Content" ("createdAt", "currentStep", "generatedContent", "generatedMusic", "generatedPicture", "generatedVideo", "generatedVoice", "id", "progress", "status", "title") SELECT "createdAt", "currentStep", "generatedContent", "generatedMusic", "generatedPicture", "generatedVideo", "generatedVoice", "id", "progress", "status", "title" FROM "Content";
DROP TABLE "Content";
ALTER TABLE "new_Content" RENAME TO "Content";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;

-- CreateIndex
CREATE UNIQUE INDEX "GeneralOptions_contentId_key" ON "GeneralOptions"("contentId");

-- CreateIndex
CREATE UNIQUE INDEX "ContentOptions_contentId_key" ON "ContentOptions"("contentId");

-- CreateIndex
CREATE UNIQUE INDEX "VisualPromptOptions_contentId_key" ON "VisualPromptOptions"("contentId");

-- CreateIndex
CREATE UNIQUE INDEX "MusicPrompt_contentId_key" ON "MusicPrompt"("contentId");
