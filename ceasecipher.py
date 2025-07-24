import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string
from collections import Counter
import threading
import time
import re
import json
from datetime import datetime

class EnhancedCaesarDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Caesar Cipher Decoder v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Enhanced English letter frequencies with digrams
        self.english_freq = {
            'A': 8.12, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.02, 'F': 2.23,
            'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03,
            'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10, 'R': 5.99,
            'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
            'Y': 1.97, 'Z': 0.07
        }
        
        # Common English digrams
        self.common_digrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'ED', 'ND', 'TO', 'EN', 'TI']
        self.common_trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR', 'ENT']
        
        # Decryption history
        self.history = []
        
        self.setup_ui()
        self.setup_styles()
        
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook', background='#2b2b2b')
        style.configure('Custom.TNotebook.Tab', background='#3b3b3b', foreground='white')
        
    def setup_ui(self):
        # Main container with gradient effect
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header with modern styling
        header_frame = tk.Frame(main_frame, bg='#1a1a1a', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🔐 Advanced Caesar Cipher Decoder v2.0", 
                              font=('Consolas', 20, 'bold'), fg='#00ff41', bg='#1a1a1a')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(header_frame, text="Enhanced with AI-powered pattern recognition & real-time analysis", 
                                 font=('Arial', 10), fg='#888888', bg='#1a1a1a')
        subtitle_label.pack()
        
        # Create enhanced notebook
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced tabs
        self.create_smart_decoder_tab()
        self.create_advanced_analysis_tab()
        self.create_pattern_recognition_tab()
        self.create_history_tab()
        
    def create_smart_decoder_tab(self):
        decoder_frame = ttk.Frame(self.notebook)
        self.notebook.add(decoder_frame, text="🤖 Smart Decoder")
        
        # Split layout
        paned_window = tk.PanedWindow(decoder_frame, orient=tk.HORIZONTAL, bg='#2b2b2b')
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Input & Controls
        left_frame = tk.Frame(paned_window, bg='#2b2b2b')
        paned_window.add(left_frame, width=600)
        
        # Input section with enhanced features
        input_frame = tk.LabelFrame(left_frame, text="📝 Input Text", font=('Arial', 11, 'bold'),
                                   fg='#00ff41', bg='#2b2b2b', bd=2)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text input with line numbers
        text_frame = tk.Frame(input_frame, bg='#2b2b2b')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(text_frame, height=8, wrap=tk.WORD,
                                                   bg='#1e1e1e', fg='#ffffff', insertbackground='#00ff41',
                                                   font=('Consolas', 10))
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        
        # Smart controls
        control_frame = tk.Frame(input_frame, bg='#2b2b2b')
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # File operations
        tk.Button(control_frame, text="📁 Load", command=self.load_file,
                 bg='#0066cc', fg='white', relief='flat', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="💾 Save", command=self.save_result,
                 bg='#009900', fg='white', relief='flat', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="🗑️ Clear", command=self.clear_all,
                 bg='#cc3300', fg='white', relief='flat', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="🎲 Sample", command=self.load_random_sample,
                 bg='#6600cc', fg='white', relief='flat', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Advanced shift controls
        shift_frame = tk.Frame(input_frame, bg='#2b2b2b')
        shift_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(shift_frame, text="🔄 Shift:", fg='#00ff41', bg='#2b2b2b', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.shift_var = tk.IntVar(value=3)
        shift_spin = tk.Spinbox(shift_frame, from_=1, to=25, textvariable=self.shift_var,
                               width=5, bg='#1e1e1e', fg='white', buttonbackground='#3b3b3b')
        shift_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(shift_frame, text="🔍 Auto-Detect", command=self.smart_auto_detect,
                 bg='#ff6600', fg='white', relief='flat', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(shift_frame, text="⚡ Quick Decode", command=self.quick_decode,
                 bg='#00aa00', fg='white', relief='flat', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Output & Analysis
        right_frame = tk.Frame(paned_window, bg='#2b2b2b')
        paned_window.add(right_frame, width=600)
        
        # Output section
        output_frame = tk.LabelFrame(right_frame, text="✨ Decoded Output", font=('Arial', 11, 'bold'),
                                    fg='#00ff41', bg='#2b2b2b', bd=2)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD,
                                                    bg='#1e1e1e', fg='#00ff41', insertbackground='#00ff41',
                                                    font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Real-time stats
        stats_frame = tk.LabelFrame(right_frame, text="📊 Live Statistics", font=('Arial', 11, 'bold'),
                                   fg='#00ff41', bg='#2b2b2b', bd=2)
        stats_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.stats_display = tk.Text(stats_frame, height=4, bg='#1e1e1e', fg='#ffffff',
                                    font=('Consolas', 9), state='disabled')
        self.stats_display.pack(fill=tk.X, padx=5, pady=5)
        
    def create_advanced_analysis_tab(self):
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📈 Advanced Analysis")
        
        # Control panel
        control_frame = tk.Frame(analysis_frame, bg='#2b2b2b', height=60)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        control_frame.pack_propagate(False)
        
        tk.Button(control_frame, text="🔬 Deep Analysis", command=self.deep_frequency_analysis,
                 bg='#0066cc', fg='white', relief='flat', font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(control_frame, text="🎯 Pattern Match", command=self.pattern_matching_analysis,
                 bg='#cc6600', fg='white', relief='flat', font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(control_frame, text="📊 Export Report", command=self.export_analysis_report,
                 bg='#009900', fg='white', relief='flat', font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Analysis results
        results_paned = tk.PanedWindow(analysis_frame, orient=tk.HORIZONTAL, bg='#2b2b2b')
        results_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Charts frame
        self.chart_frame = tk.Frame(results_paned, bg='#2b2b2b')
        results_paned.add(self.chart_frame, width=800)
        
        # Enhanced statistics
        stats_frame = tk.LabelFrame(results_paned, text="🔍 Detailed Analysis", font=('Arial', 11, 'bold'),
                                   fg='#00ff41', bg='#2b2b2b', width=400)
        results_paned.add(stats_frame, width=400)
        
        self.detailed_stats = scrolledtext.ScrolledText(stats_frame, bg='#1e1e1e', fg='#ffffff',
                                                       font=('Consolas', 9), insertbackground='white')
        self.detailed_stats.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_pattern_recognition_tab(self):
        pattern_frame = ttk.Frame(self.notebook)
        self.notebook.add(pattern_frame, text="🧠 Pattern Recognition")
        
        # AI-powered pattern recognition interface
        tk.Label(pattern_frame, text="🤖 AI Pattern Recognition Engine", 
                font=('Arial', 14, 'bold'), fg='#00ff41', bg='#2b2b2b').pack(pady=10)
        
        # Pattern analysis controls
        pattern_controls = tk.Frame(pattern_frame, bg='#2b2b2b')
        pattern_controls.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(pattern_controls, text="🔍 Analyze Patterns", command=self.analyze_patterns,
                 bg='#0066cc', fg='white', relief='flat', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(pattern_controls, text="🎯 Smart Guess", command=self.intelligent_guess,
                 bg='#ff6600', fg='white', relief='flat', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Pattern results
        self.pattern_results = scrolledtext.ScrolledText(pattern_frame, bg='#1e1e1e', fg='#ffffff',
                                                        font=('Consolas', 10), insertbackground='white')
        self.pattern_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📚 History")
        
        # History controls
        history_controls = tk.Frame(history_frame, bg='#2b2b2b')
        history_controls.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(history_controls, text="🔄 Refresh", command=self.refresh_history,
                 bg='#0066cc', fg='white', relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(history_controls, text="📤 Export", command=self.export_history,
                 bg='#009900', fg='white', relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(history_controls, text="🗑️ Clear", command=self.clear_history,
                 bg='#cc3300', fg='white', relief='flat').pack(side=tk.LEFT, padx=5)
        
        # History display
        self.history_display = scrolledtext.ScrolledText(history_frame, bg='#1e1e1e', fg='#ffffff',
                                                        font=('Consolas', 9), insertbackground='white')
        self.history_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def caesar_decrypt(self, text, shift):
        """Enhanced Caesar decryption with better handling"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                result += decrypted_char
            else:
                result += char
        return result
    
    def get_enhanced_frequency(self, text):
        """Enhanced frequency analysis with additional metrics"""
        letters_only = ''.join([c.upper() for c in text if c.isalpha()])
        if not letters_only:
            return {}, {}, {}
        
        total_letters = len(letters_only)
        freq_count = Counter(letters_only)
        
        # Letter frequency
        letter_freq = {letter: (freq_count.get(letter, 0) / total_letters) * 100 
                      for letter in string.ascii_uppercase}
        
        # Digram frequency
        digrams = [letters_only[i:i+2] for i in range(len(letters_only)-1)]
        digram_count = Counter(digrams)
        digram_freq = {digram: count for digram, count in digram_count.most_common(10)}
        
        # Trigram frequency
        trigrams = [letters_only[i:i+3] for i in range(len(letters_only)-2)]
        trigram_count = Counter(trigrams)
        trigram_freq = {trigram: count for trigram, count in trigram_count.most_common(10)}
        
        return letter_freq, digram_freq, trigram_freq
    
    def calculate_enhanced_score(self, text):
        """Enhanced scoring system"""
        letter_freq, digram_freq, trigram_freq = self.get_enhanced_frequency(text)
        
        # Chi-squared for letters
        chi_squared = 0
        for letter in string.ascii_uppercase:
            expected = self.english_freq[letter]
            observed = letter_freq.get(letter, 0)
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        # Bonus for common English patterns
        pattern_score = 0
        text_upper = text.upper()
        
        # Check for common digrams
        for digram in self.common_digrams:
            pattern_score += text_upper.count(digram) * 2
        
        # Check for common trigrams
        for trigram in self.common_trigrams:
            pattern_score += text_upper.count(trigram) * 3
        
        # Combined score (lower is better)
        return chi_squared - pattern_score
    
    def smart_auto_detect(self):
        """Enhanced auto-detection with pattern recognition"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        best_shift = 0
        best_score = float('inf')
        results = []
        
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            score = self.calculate_enhanced_score(decoded)
            results.append((shift, score, decoded[:50]))
            
            if score < best_score:
                best_score = score
                best_shift = shift
        
        self.shift_var.set(best_shift)
        self.quick_decode()
        
        confidence = max(0, 100 - best_score)
        messagebox.showinfo("🧠 AI Analysis Complete", 
                           f"🎯 Intelligent guess: Shift {best_shift}\n"
                           f"🔬 AI Confidence: {confidence:.1f}%\n"
                           f"📊 Analysis score: {best_score:.2f}")
    
    def add_to_history(self, action, score):
        """Add entry to decryption history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            'time': timestamp,
            'action': action,
            'score': score,
            'input_preview': self.input_text.get(1.0, "1.50"),
            'output_preview': self.output_text.get(1.0, "1.50")
        }
        self.history.append(entry)
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        self.history_display.delete(1.0, tk.END)
        
        if not self.history:
            self.history_display.insert(tk.END, "📚 No decryption history yet...\n")
            return
        
        self.history_display.insert(tk.END, "📚 DECRYPTION HISTORY\n")
        self.history_display.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, entry in enumerate(reversed(self.history[-10:])):  # Show last 10
            self.history_display.insert(tk.END, f"🕐 {entry['time']} | {entry['action']}\n")
            self.history_display.insert(tk.END, f"   Score: {entry['score']:.2f}\n")
            self.history_display.insert(tk.END, f"   Input: {entry['input_preview'].strip()[:40]}...\n")
            self.history_display.insert(tk.END, f"   Output: {entry['output_preview'].strip()[:40]}...\n\n")
    
    def pattern_matching_analysis(self):
        """Advanced pattern matching analysis"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        # Clear previous analysis
        self.detailed_stats.delete(1.0, tk.END)
        
        analysis = "🔍 PATTERN MATCHING ANALYSIS\n"
        analysis += "=" * 40 + "\n\n"
        
        # Test all shifts and find patterns
        pattern_matches = []
        
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            decoded_upper = decoded.upper()
            
            # Count pattern matches
            digram_matches = sum(1 for digram in self.common_digrams if digram in decoded_upper)
            trigram_matches = sum(1 for trigram in self.common_trigrams if trigram in decoded_upper)
            
            # Calculate pattern density
            total_patterns = digram_matches + trigram_matches
            pattern_density = total_patterns / max(1, len(decoded.split()))
            
            pattern_matches.append((shift, total_patterns, pattern_density, decoded))
        
        # Sort by pattern matches
        pattern_matches.sort(key=lambda x: x[1], reverse=True)
        
        analysis += "🎯 PATTERN MATCH RANKING:\n"
        analysis += "-" * 30 + "\n"
        
        for i, (shift, matches, density, decoded) in enumerate(pattern_matches[:8]):
            analysis += f"\n🔑 Shift {shift:2d}: {matches:2d} patterns (density: {density:.3f})\n"
            analysis += f"   Preview: {decoded[:60]}...\n"
        
        # Best candidate analysis
        best_shift = pattern_matches[0][0]
        analysis += f"\n🏆 RECOMMENDED SHIFT: {best_shift}\n"
        analysis += f"   Reasoning: Highest pattern match count\n"
        analysis += f"   Confidence: High\n"
        
        self.detailed_stats.insert(1.0, analysis)
    
    def export_analysis_report(self):
        """Export comprehensive analysis report"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                report = self.generate_comprehensive_report(text)
                
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(report, f, indent=2)
                else:
                    with open(filename, 'w') as f:
                        f.write(self.format_report_text(report))
                
                messagebox.showinfo("Success", f"Analysis report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not export report: {str(e)}")
    
    def generate_comprehensive_report(self, text):
        """Generate comprehensive analysis report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'input_text': text,
            'analysis': {}
        }
        
        # Analyze all shifts
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            letter_freq, digram_freq, trigram_freq = self.get_enhanced_frequency(decoded)
            
            report['analysis'][f'shift_{shift}'] = {
                'shift': shift,
                'decoded_text': decoded,
                'quality_score': self.calculate_enhanced_score(decoded),
                'readability_score': self.calculate_readability(decoded),
                'word_score': self.calculate_word_score(decoded),
                'letter_frequency': letter_freq,
                'top_digrams': dict(list(digram_freq.items())[:5]),
                'top_trigrams': dict(list(trigram_freq.items())[:5])
            }
        
        return report
    
    def format_report_text(self, report):
        """Format report as readable text"""
        text = f"🔐 CAESAR CIPHER ANALYSIS REPORT\n"
        text += f"Generated: {report['timestamp']}\n"
        text += "=" * 50 + "\n\n"
        
        text += f"📝 Input Text Length: {len(report['input_text'])} characters\n"
        text += f"📝 Input Preview: {report['input_text'][:100]}...\n\n"
        
        # Find best candidates
        candidates = []
        for shift_key, data in report['analysis'].items():
            total_score = data['quality_score'] + data['readability_score'] + data['word_score']
            candidates.append((data['shift'], total_score, data['decoded_text']))
        
        candidates.sort(key=lambda x: x[1])
        
        text += "🏆 TOP 5 CANDIDATES:\n"
        text += "-" * 30 + "\n"
        
        for i, (shift, score, decoded) in enumerate(candidates[:5]):
            text += f"\n🔑 Rank {i+1}: Shift {shift} (Score: {score:.2f})\n"
            text += f"   {decoded[:80]}...\n"
        
        return text
    
    def load_file(self):
        """Load text from file with enhanced support"""
        filename = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(1.0, content)
                    self.add_to_history(f"Loaded file: {filename}", 0)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def save_result(self):
        """Save decoded result to file"""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No decoded text to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Result saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def clear_all(self):
        """Clear all text fields"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.stats_display.config(state='normal')
        self.stats_display.delete(1.0, tk.END)
        self.stats_display.config(state='disabled')
    
    def load_random_sample(self):
        """Load random sample encrypted text"""
        samples = [
            ("Classic Quote", "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ. FDHVDU FLSKHU LV RQH RI WKH VLPSOHVW DQG PRVW ZLGHOB NQRZQ HQFUBSWLRQ WHFKQLTXHV."),
            ("Shakespeare", "WR EH RU QRW WR EH WKDW LV WKH TXHVWLRQ ZKHWKHU WLV QREOHU LQ WKH PLQG WR VXIIHU WKH VOLQJV DQG DUURZV"),
            ("Declaration", "ZH KROG WKHVH WUXWKV WR EH VHOI HYLGHQW WKDW DOO PHQ DUH FUHDWHG HTXDO WKDW WKHB DUH HQGRZHG EB WKHLU FUHDWRU"),
            ("Tech Quote", "FRPSXWHUV DUH LQFUHGLEBO IDVW DFFXUDWH DQG VWXSLG KXPDQV DUH LQFUHGLEBO VORZ LQDFFXUDWH DQG EULOODQW"),
            ("Mystery Text", "EUXWH IRUFH DWWDFNV DUH FRPPRQ LQ FUSWRJUDSKB ZKHQ BRX FDQQRW ILQG WKH NHB WUB DOO SRVVLEOH NHBV")
        ]
        
        import random
        name, sample = random.choice(samples)
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, sample)
        self.add_to_history(f"Loaded sample: {name}", 0)
    
    def export_history(self):
        """Export decryption history"""
        if not self.history:
            messagebox.showwarning("Warning", "No history to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.history, f, indent=2)
                messagebox.showinfo("Success", f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not export history: {str(e)}")
    
    def clear_history(self):
        """Clear decryption history"""
        if messagebox.askyesno("Confirm", "Clear all decryption history?"):
            self.history.clear()
            self.refresh_history()


    
    def quick_decode(self):
        """Quick decode with real-time stats"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            return
        
        shift = self.shift_var.get()
        decoded = self.caesar_decrypt(text, shift)
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, decoded)
        
        # Update live stats
        self.update_live_stats(text, decoded, shift)
        
        # Add to history
        self.add_to_history(f"Manual decode with shift {shift}", self.calculate_enhanced_score(decoded))
    
    def update_live_stats(self, original, decoded, shift):
        """Update real-time statistics"""
        self.stats_display.config(state='normal')
        self.stats_display.delete(1.0, tk.END)
        
        stats = f"🔑 Shift: {shift} | 📝 Length: {len(original)} | "
        stats += f"🔤 Letters: {len([c for c in original if c.isalpha()])}\n"
        
        score = self.calculate_enhanced_score(decoded)
        stats += f"📊 Quality Score: {score:.2f} | "
        
        # Check for common English words
        common_words = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'FOR', 'IS', 'ON', 'THAT']
        word_matches = sum(1 for word in common_words if word in decoded.upper())
        stats += f"🎯 Word Matches: {word_matches}/10\n"
        
        self.stats_display.insert(1.0, stats)
        self.stats_display.config(state='disabled')
    
    def on_text_change(self, event):
        """Handle text changes for real-time analysis"""
        if hasattr(self, 'output_text'):
            self.quick_decode()
    
    def deep_frequency_analysis(self):
        """Perform deep frequency analysis with visualization"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        # Clear previous charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        letter_freq, digram_freq, trigram_freq = self.get_enhanced_frequency(text)
        
        # Create enhanced visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('#2b2b2b')
        
        # Letter frequency
        letters = list(string.ascii_uppercase)
        text_freq = [letter_freq[letter] for letter in letters]
        english_freq = [self.english_freq[letter] for letter in letters]
        
        ax1.bar(letters, text_freq, color='#ff6b6b', alpha=0.8, label='Input Text')
        ax1.bar(letters, english_freq, color='#4ecdc4', alpha=0.6, label='English')
        ax1.set_title('Letter Frequency Comparison', color='white', fontsize=11)
        ax1.legend()
        ax1.tick_params(colors='white', labelsize=8)
        ax1.set_facecolor('#3b3b3b')
        
        # Digram frequency
        if digram_freq:
            digrams = list(digram_freq.keys())[:8]
            counts = list(digram_freq.values())[:8]
            ax2.bar(digrams, counts, color='#95e1d3', alpha=0.8)
            ax2.set_title('Most Common Digrams', color='white', fontsize=11)
            ax2.tick_params(colors='white', labelsize=8)
            ax2.set_facecolor('#3b3b3b')
        
        # Trigram frequency
        if trigram_freq:
            trigrams = list(trigram_freq.keys())[:6]
            counts = list(trigram_freq.values())[:6]
            ax3.bar(trigrams, counts, color='#f8b500', alpha=0.8)
            ax3.set_title('Most Common Trigrams', color='white', fontsize=11)
            ax3.tick_params(colors='white', labelsize=8)
            ax3.set_facecolor('#3b3b3b')
        
        # Pattern analysis heatmap
        pattern_data = []
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            score = self.calculate_enhanced_score(decoded)
            pattern_data.append(score)
        
        ax4.plot(range(1, 26), pattern_data, color='#00ff41', linewidth=2, marker='o', markersize=4)
        ax4.set_title('Shift Quality Analysis', color='white', fontsize=11)
        ax4.set_xlabel('Shift Value', color='white')
        ax4.set_ylabel('Quality Score', color='white')
        ax4.tick_params(colors='white', labelsize=8)
        ax4.set_facecolor('#3b3b3b')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed in GUI
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.update_detailed_stats(text, letter_freq, digram_freq, trigram_freq)
    
    def update_detailed_stats(self, text, letter_freq, digram_freq, trigram_freq):
        """Update detailed statistics display"""
        self.detailed_stats.delete(1.0, tk.END)
        
        stats = "🔬 DEEP ANALYSIS RESULTS\n"
        stats += "=" * 40 + "\n\n"
        
        stats += f"📊 Text Statistics:\n"
        stats += f"  • Total chars: {len(text)}\n"
        stats += f"  • Letters: {len([c for c in text if c.isalpha()])}\n"
        stats += f"  • Words: {len(text.split())}\n"
        stats += f"  • Sentences: {len(re.split(r'[.!?]+', text))}\n\n"
        
        stats += "🔤 Top Letter Frequencies:\n"
        sorted_letters = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
        for letter, freq in sorted_letters[:10]:
            expected = self.english_freq[letter]
            diff = freq - expected
            stats += f"  {letter}: {freq:5.2f}% ({diff:+5.2f})\n"
        
        stats += f"\n🔗 Common Digrams:\n"
        for digram, count in list(digram_freq.items())[:8]:
            stats += f"  {digram}: {count}\n"
        
        stats += f"\n🔗 Common Trigrams:\n"
        for trigram, count in list(trigram_freq.items())[:6]:
            stats += f"  {trigram}: {count}\n"
        
        self.detailed_stats.insert(1.0, stats)
    
    def analyze_patterns(self):
        """AI-powered pattern analysis"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        self.pattern_results.delete(1.0, tk.END)
        self.pattern_results.insert(tk.END, "🧠 AI PATTERN ANALYSIS\n")
        self.pattern_results.insert(tk.END, "=" * 50 + "\n\n")
        
        # Analyze all possible shifts
        candidates = []
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            score = self.calculate_enhanced_score(decoded)
            
            # Additional pattern checks
            readability_score = self.calculate_readability(decoded)
            word_score = self.calculate_word_score(decoded)
            
            combined_score = score + readability_score + word_score
            candidates.append((shift, combined_score, decoded))
        
        # Sort by best score
        candidates.sort(key=lambda x: x[1])
        
        self.pattern_results.insert(tk.END, "🎯 TOP CANDIDATES:\n")
        self.pattern_results.insert(tk.END, "-" * 30 + "\n")
        
        for i, (shift, score, decoded) in enumerate(candidates[:5]):
            confidence = max(0, 100 - score)
            self.pattern_results.insert(tk.END, f"\n🔑 Rank {i+1}: Shift {shift} (Confidence: {confidence:.1f}%)\n")
            self.pattern_results.insert(tk.END, f"Preview: {decoded[:80]}...\n")
    
    def calculate_readability(self, text):
        """Calculate readability score"""
        # Simple readability based on word patterns
        words = text.split()
        if not words:
            return 100
        
        score = 0
        for word in words:
            if len(word) < 2:
                score += 5
            elif len(word) > 15:
                score += 3
            else:
                score -= 1
        
        return max(0, score)
    
    def calculate_word_score(self, text):
        """Calculate word pattern score"""
        common_words = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'FOR', 'IS', 'ON', 'THAT', 'WITH', 'IT', 'BE', 'AS', 'YOU', 'HAVE', 'ARE', 'AT', 'THIS', 'OR']
        words = text.upper().split()
        
        if not words:
            return 100
        
        matches = sum(1 for word in words if word in common_words)
        return max(0, 50 - (matches * 2))
    
    def intelligent_guess(self):
        """Make intelligent guess based on all analysis"""
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
        
        # Run comprehensive analysis
        best_shift = 0
        best_score = float('inf')
        
        for shift in range(1, 26):
            decoded = self.caesar_decrypt(text, shift)
            
            # Combined scoring
            freq_score = self.calculate_enhanced_score(decoded)
            read_score = self.calculate_readability(decoded)
            word_score = self.calculate_word_score(decoded)
            
            total_score = freq_score + read_score + word_score
            
            if total_score < best_score:
                best_score = total_score
                best_shift = shift
        
        self.shift_var.set(best_shift)
        self.quick_decode()


def main():
    root = tk.Tk()
    app = EnhancedCaesarDecoder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
        
    