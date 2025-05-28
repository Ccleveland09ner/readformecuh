import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { Button } from './components/ui/button';
import { Card } from './components/ui/card';
import { Progress } from './components/ui/progress';
import { FileAudio, FileText, Play, Download } from 'lucide-react';

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [showSummarizeOptions, setShowSummarizeOptions] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileUpload = async (endpoint: string, file: File) => {
    setIsProcessing(true);
    setProgress(0);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const blob = await response.blob();
      setAudioUrl(URL.createObjectURL(blob));
      setFileName(file.name);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
      setProgress(100);
    }
  };

  const handleTextToSpeech = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAudioUrl(null);
      setSummary(null);
      await handleFileUpload('to-audio', file);
    }
  };

  const handleSummarize = async (e: React.ChangeEvent<HTMLInputElement>, withAudio: boolean) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsProcessing(true);
    setProgress(0);
    setAudioUrl(null);
    setSummary(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = withAudio ? 'summarise-audio' : 'summarise';
      const response = await fetch(`http://localhost:8000/api/v1/${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Summarization failed');

      if (withAudio) {
        const blob = await response.blob();
        setAudioUrl(URL.createObjectURL(blob));
      } else {
        const text = await response.text();
        setSummary(text);
      }
      setFileName(file.name);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
      setProgress(100);
    }
  };

  const downloadSummary = () => {
    if (!summary) return;
    const blob = new Blob([summary], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'summary.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-pulse flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12 max-w-3xl"
      >
        <h1 className="text-4xl font-bold mb-4 text-gray-800">
          Turn any document into speech or a concise summary in seconds.
        </h1>
      </motion.div>

      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Button
            size="lg"
            className="rounded-full px-8 py-6 bg-blue-600 hover:bg-blue-700 shadow-lg"
            onClick={() => document.getElementById('tts-input')?.click()}
            disabled={isProcessing}
          >
            <FileAudio className="mr-2" /> Text-to-Speech
          </Button>
          <input
            id="tts-input"
            type="file"
            className="hidden"
            accept=".pdf,.docx,.xml,.txt"
            onChange={handleTextToSpeech}
          />
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Button
            size="lg"
            className="rounded-full px-8 py-6 bg-purple-600 hover:bg-purple-700 shadow-lg"
            onClick={() => setShowSummarizeOptions(true)}
            disabled={isProcessing}
          >
            <FileText className="mr-2" /> Summarize
          </Button>
        </motion.div>
      </div>

      <AnimatePresence>
        {showSummarizeOptions && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="flex flex-col sm:flex-row gap-4 mb-8"
          >
            <Button
              variant="outline"
              className="rounded-full shadow-md"
              onClick={() => document.getElementById('summarize-text-input')?.click()}
              disabled={isProcessing}
            >
              Summarize (Text)
            </Button>
            <Button
              variant="outline"
              className="rounded-full shadow-md"
              onClick={() => document.getElementById('summarize-audio-input')?.click()}
              disabled={isProcessing}
            >
              Summarize + TTS
            </Button>
            <input
              id="summarize-text-input"
              type="file"
              className="hidden"
              accept=".pdf,.docx,.xml,.txt"
              onChange={(e) => handleSummarize(e, false)}
            />
            <input
              id="summarize-audio-input"
              type="file"
              className="hidden"
              accept=".pdf,.docx,.xml,.txt"
              onChange={(e) => handleSummarize(e, true)}
            />
          </motion.div>
        )}

        {isProcessing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full max-w-md"
          >
            <Card className="p-4">
              <p className="text-center mb-2">Processing {fileName}...</p>
              <Progress value={progress} className="h-2" />
            </Card>
          </motion.div>
        )}

        {audioUrl && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-md"
          >
            <Card className="p-4">
              <p className="font-medium mb-2">{fileName}</p>
              <audio controls className="w-full mb-4" src={audioUrl} />
              <div className="flex gap-2">
                <Button
                  onClick={() => window.open(audioUrl)}
                  className="w-full rounded-xl"
                >
                  <Download className="mr-2" /> Download MP3
                </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {summary && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-2xl"
          >
            <Card className="p-4">
              <p className="font-medium mb-2">{fileName}</p>
              <div className="max-h-60 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
                <p className="whitespace-pre-wrap">{summary}</p>
              </div>
              <Button
                onClick={downloadSummary}
                className="w-full rounded-xl"
              >
                <Download className="mr-2" /> Download Summary
              </Button>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;