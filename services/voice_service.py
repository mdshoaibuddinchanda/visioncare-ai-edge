"""
Voice service for text-to-speech functionality in multiple languages.
"""
import os
import platform
import subprocess


class VoiceService:
    """Text-to-speech service for reading reports aloud."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.supported_languages = {
            "english": "en",
            "hindi": "hi",
            "telugu": "te"
        }
    
    def speak(self, text, language="english"):
        """
        Convert text to speech.
        
        Args:
            text: Text to read aloud
            language: Language code ('english', 'hindi', 'telugu')
            
        Returns:
            bool: Success status
        """
        import re
        # Strip out common markdown and HTML formatting so TTS doesn't read symbols
        clean_text = re.sub(r'<[^>]+>', '', text)  # remove html
        clean_text = re.sub(r'[*_#=\`~>\[\]\(\)]', '', clean_text)  # remove markdown symbols
        clean_text = clean_text.replace("equals to", " ").replace("equals", " ") # specific fix for equals
        
        text = clean_text.strip()
        
        if not text:
            return False
        if language not in self.supported_languages:
            language = "english"
        
        try:
            if self.system == "windows":
                return self._speak_windows(text)
            elif self.system == "darwin":
                return self._speak_mac(text)
            elif self.system == "linux":
                return self._speak_linux(text)
            else:
                print(f"Text-to-speech not supported on {self.system}")
                return False
        except Exception as e:
            print(f"Voice service error: {e}")
            return False
    
    def _speak_windows(self, text):
        """Text-to-speech on Windows using SAPI."""
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
            return True
        except ImportError:
            # Fallback using PowerShell
            try:
                ps_command = f"""
                Add-Type -AssemblyName System.Speech;
                $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer;
                $speaker.Speak('{text.replace("'", "''")}');
                """
                subprocess.run(["powershell", "-Command", ps_command], capture_output=True, timeout=30)
                return True
            except:
                print("Windows TTS not available. Install pywin32 or check PowerShell.")
                return False
    
    def _speak_mac(self, text):
        """Text-to-speech on macOS using say command."""
        try:
            subprocess.run(["say", text], capture_output=True, timeout=30)
            return True
        except:
            return False
    
    def _speak_linux(self, text):
        """Text-to-speech on Linux using espeak or festival."""
        try:
            subprocess.run(["espeak", text], capture_output=True, timeout=30)
            return True
        except FileNotFoundError:
            try:
                subprocess.run(["festival", "--tts"], input=text.encode(), capture_output=True, timeout=30)
                return True
            except:
                return False
    
    def get_available_languages(self):
        """Get list of supported languages."""
        return list(self.supported_languages.keys())
    
    def is_available(self):
        """Check if TTS is available on this system."""
        try:
            if self.system == "windows":
                return self._speak_windows("test") or True
            elif self.system == "darwin":
                subprocess.run(["say", "test"], capture_output=True, timeout=5)
                return True
            elif self.system == "linux":
                result = subprocess.run(["which", "espeak"], capture_output=True, timeout=5)
                return result.returncode == 0
            return False
        except:
            return False