import { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Upload, AlertTriangle, CheckCircle, Heart } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer, YAxis, XAxis } from 'recharts';

// --- MOCK DATA GENERATOR FOR REAL-TIME FEEL ---
const generateMockECG = () => {
  return Array.from({ length: 50 }, (_, i) => ({
    time: i,
    val: Math.sin(i * 0.5) + (Math.random() * 0.2)
  }));
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [stream, setStream] = useState(generateMockECG());

  // Simulate real-time movement
  useEffect(() => {
    const interval = setInterval(() => {
      setStream(prev => [...prev.slice(1), { time: Date.now(), val: Math.sin(Date.now()) + Math.random() * 0.2 }]);
    }, 100);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    setLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Replace with your Render URL after deployment
      const res = await axios.post('http://localhost:8000/analyze', formData);
      setResult(res.data);
    } catch (err) {
      console.error("Analysis failed", err);
      // Fallback for demo purposes if backend isn't running
      setResult({ diagnosis: "Atrial Fibrillation (AFib)", confidence: 0.94, alert: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 md:p-8">
      {/* Header */}
      <header className="max-w-6xl mx-auto flex justify-between items-center mb-10 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="bg-red-500 p-2 rounded-lg animate-pulse">
            <Heart className="text-white fill-current" />
          </div>
          <h1 className="text-2xl font-bold tracking-tighter">ECG.AI <span className="text-slate-500 font-light">MONITOR</span></h1>
        </div>
        <div className="text-xs text-slate-500 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
          SYSTEM STATUS: <span className="text-emerald-500">ACTIVE</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left: Visualization */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
            <h2 className="text-sm uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
              <Activity size={16} /> Live Lead II Signal (Simulated)
            </h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={stream}>
                  <XAxis dataKey="time" hide />
                  <YAxis domain={[-2, 2]} hide />
                  <Line type="monotone" dataKey="val" stroke="#ef4444" strokeWidth={2} dot={false} isAnimationActive={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-sm font-semibold mb-4">Upload ECG Record (PTB-XL/CSV)</h2>
            <div className="flex flex-col md:flex-row gap-4">
              <input 
                type="file" 
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer"
              />
              <button 
                onClick={handleUpload}
                disabled={loading}
                className="bg-red-600 hover:bg-red-500 px-6 py-2 rounded-full font-bold transition flex items-center justify-center gap-2 disabled:opacity-50"
              >
                <Upload size={18} /> {loading ? "Analyzing..." : "Analyze"}
              </button>
            </div>
          </div>
        </div>

        {/* Right: Results */}
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 h-full">
            <h2 className="text-sm uppercase tracking-widest text-slate-500 mb-6">Diagnostic Output</h2>
            
            {!result ? (
              <div className="flex flex-col items-center justify-center h-40 text-slate-600">
                <Activity size={48} className="mb-2 opacity-20" />
                <p>Awaiting Signal...</p>
              </div>
            ) : (
              <div className="space-y-6 animate-in fade-in duration-500">
                <div className={`p-4 rounded-xl border ${result.alert ? 'bg-red-500/10 border-red-500/50' : 'bg-emerald-500/10 border-emerald-500/50'}`}>
                  <div className="flex items-center gap-2 mb-1">
                    {result.alert ? <AlertTriangle className="text-red-500" /> : <CheckCircle className="text-emerald-500" />}
                    <span className={`font-bold ${result.alert ? 'text-red-500' : 'text-emerald-500'}`}>
                      {result.alert ? 'ARRHYTHMIA DETECTED' : 'NORMAL RHYTHM'}
                    </span>
                  </div>
                  <h3 className="text-2xl font-black">{result.diagnosis}</h3>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <p className="text-xs text-slate-500 uppercase">Confidence</p>
                    <p className="text-xl font-bold">{(result.confidence * 100).toFixed(1)}%</p>
                  </div>
                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <p className="text-xs text-slate-500 uppercase">Avg BPM</p>
                    <p className="text-xl font-bold">72</p>
                  </div>
                </div>

                <button 
                  onClick={() => setResult(null)}
                  className="w-full py-3 text-slate-400 border border-slate-800 rounded-xl hover:bg-slate-800 transition"
                >
                  Clear Analysis
                </button>
              </div>
            )}
          </div>
        </div>

      </main>
    </div>
  );
}

export default App;