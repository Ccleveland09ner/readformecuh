import { motion } from "framer-motion";
import { Button } from "./components/ui/button";
import { useState } from "react";

export default function App() {
  const [isProcessing, setIsProcessing] = useState(false);

  const handleTTS = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/v1/to-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to process file');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'speech.mp3';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSummarize = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/v1/summarise', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to process file');

      const text = await response.text();
      const blob = new Blob([text], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'summary.txt';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen animate-pulse-gray">
      <div className="container mx-auto px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Turn any document into speech or a concise summary in seconds
          </h1>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-12">
            <div>
              <input
                type="file"
                id="tts-input"
                accept=".pdf,.docx,.xml,.txt"
                className="hidden"
                onChange={handleTTS}
                disabled={isProcessing}
              />
              <Button
                size="lg"
                onClick={() => document.getElementById('tts-input')?.click()}
                disabled={isProcessing}
              >
                Text-to-Speech
              </Button>
            </div>

            <div>
              <input
                type="file"
                id="summary-input"
                accept=".pdf,.docx,.xml,.txt"
                className="hidden"
                onChange={handleSummarize}
                disabled={isProcessing}
              />
              <Button
                size="lg"
                variant="secondary"
                onClick={() => document.getElementById('summary-input')?.click()}
                disabled={isProcessing}
              >
                Summarize
              </Button>
            </div>
          </div>

          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-8"
            >
              <div className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                <span className="text-gray-600">Processing your document...</span>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
}