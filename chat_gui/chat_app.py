import sys
import os
import threading
import asyncio
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app'))

import customtkinter as ctk
from dotenv import load_dotenv

load_dotenv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_dark": "#0f0f0f",
    "bg_secondary": "#1a1a1a",
    "bg_chat": "#121212",
    "user_bubble": "#2563eb",
    "ai_bubble": "#262626",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0a0",
    "accent": "#3b82f6",
    "accent_hover": "#2563eb",
    "border": "#333333",
    "success": "#22c55e",
    "input_bg": "#1e1e1e",
}


class ChatMessage(ctk.CTkFrame):
    def __init__(self, parent, message: str, is_user: bool = True, timestamp: str = None):
        super().__init__(parent, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        
        bubble_color = COLORS["user_bubble"] if is_user else COLORS["ai_bubble"]
        anchor = "e" if is_user else "w"
        
        message_frame = ctk.CTkFrame(self, fg_color="transparent")
        message_frame.grid(row=0, column=0, sticky=anchor, padx=10, pady=5)
        
        bubble = ctk.CTkFrame(message_frame, fg_color=bubble_color, corner_radius=16)
        bubble.pack(side="top", anchor=anchor)
        
        label = ctk.CTkLabel(
            bubble,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_primary"],
            wraplength=400,
            justify="left" if not is_user else "right",
            anchor="w"
        )
        label.pack(padx=16, pady=10)
        
        if timestamp:
            time_label = ctk.CTkLabel(
                message_frame,
                text=timestamp,
                font=ctk.CTkFont(size=10),
                text_color=COLORS["text_secondary"]
            )
            time_label.pack(side="top", anchor=anchor, padx=5)


class ScrollableChatFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.messages = []
        self.row_count = 0
    
    def add_message(self, message: str, is_user: bool = True):
        timestamp = datetime.now().strftime("%I:%M %p")
        msg_widget = ChatMessage(self, message, is_user, timestamp)
        msg_widget.grid(row=self.row_count, column=0, sticky="ew", pady=2)
        self.messages.append(msg_widget)
        self.row_count += 1
        self.after(100, lambda: self._parent_canvas.yview_moveto(1.0))
    
    def clear_messages(self):
        for msg in self.messages:
            msg.destroy()
        self.messages = []
        self.row_count = 0


class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ByteMap AI Assistant")
        self.geometry("900x700")
        self.minsize(600, 500)
        
        self.configure(fg_color=COLORS["bg_dark"])
        
        self.agent = None
        self.current_model = "ollama"
        self.is_processing = False
        
        self.setup_ui()
        self.load_agent()
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], height=70, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)
        
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        title = ctk.CTkLabel(
            logo_frame,
            text="🤖 ByteMap AI",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="  Assistant",
            font=ctk.CTkFont(size=22),
            text_color=COLORS["accent"]
        )
        subtitle.pack(side="left")
        
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        model_label = ctk.CTkLabel(
            controls_frame,
            text="Model:",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )
        model_label.pack(side="left", padx=(0, 10))
        
        self.model_selector = ctk.CTkSegmentedButton(
            controls_frame,
            values=["Ollama", "Gemini"],
            command=self.on_model_change,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["bg_dark"],
            selected_color=COLORS["accent"],
            selected_hover_color=COLORS["accent_hover"],
            unselected_color=COLORS["bg_dark"],
            unselected_hover_color=COLORS["border"],
            corner_radius=8
        )
        self.model_selector.set("Ollama")
        self.model_selector.pack(side="left", padx=(0, 15))
        
        self.clear_btn = ctk.CTkButton(
            controls_frame,
            text="🗑️ Clear",
            width=80,
            height=32,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["bg_dark"],
            hover_color=COLORS["border"],
            corner_radius=8,
            command=self.clear_chat
        )
        self.clear_btn.pack(side="left")
    
    def create_chat_area(self):
        chat_container = ctk.CTkFrame(self, fg_color=COLORS["bg_chat"], corner_radius=0)
        chat_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        chat_container.grid_columnconfigure(0, weight=1)
        chat_container.grid_rowconfigure(0, weight=1)
        
        self.chat_frame = ScrollableChatFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["text_secondary"]
        )
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.chat_frame.add_message(
            "👋 Welcome to ByteMap AI Assistant!\n\n"
            "I can help you manage blogs, projects, services, testimonials, FAQs, and more.\n\n"
            "Try saying: 'List all blogs' or 'Create blog about AI trends'",
            is_user=False
        )
    
    def create_input_area(self):
        input_container = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], height=80, corner_radius=0)
        input_container.grid(row=2, column=0, sticky="ew")
        input_container.grid_columnconfigure(0, weight=1)
        input_container.grid_propagate(False)
        
        input_inner = ctk.CTkFrame(input_container, fg_color="transparent")
        input_inner.pack(fill="x", padx=20, pady=15)
        input_inner.grid_columnconfigure(0, weight=1)
        
        self.message_entry = ctk.CTkEntry(
            input_inner,
            placeholder_text="Type your message here...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=12,
            text_color=COLORS["text_primary"]
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ctk.CTkButton(
            input_inner,
            text="Send ➤",
            width=100,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=12,
            command=self.send_message
        )
        self.send_btn.pack(side="right")
        
        self.status_label = ctk.CTkLabel(
            input_container,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(side="bottom", pady=(0, 5))
    
    def on_model_change(self, value: str):
        self.current_model = value.lower()
        self.status_label.configure(text=f"Switched to {value}")
        self.after(2000, lambda: self.status_label.configure(text=""))
        self.load_agent()
    
    def load_agent(self):
        def _load():
            try:
                from agent.llm import set_llm_provider
                set_llm_provider(self.current_model)
            except ImportError:
                pass
            
            from agent.agent import ByteMapAgent
            self.agent = ByteMapAgent()
            self.after(0, lambda: self.status_label.configure(text=f"✅ {self.current_model.title()} model loaded"))
            self.after(2000, lambda: self.status_label.configure(text=""))
        
        threading.Thread(target=_load, daemon=True).start()
    
    def send_message(self):
        if self.is_processing:
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        self.message_entry.delete(0, "end")
        self.chat_frame.add_message(message, is_user=True)
        
        self.is_processing = True
        self.send_btn.configure(state="disabled", text="...")
        self.status_label.configure(text="🔄 Processing...")
        
        threading.Thread(target=self._process_message, args=(message,), daemon=True).start()
    
    def _process_message(self, message: str):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.agent.process_message(message))
            loop.close()
            
            self.after(0, lambda: self._handle_response(response))
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.after(0, lambda: self._handle_response(error_msg))
    
    def _handle_response(self, response: str):
        self.chat_frame.add_message(response, is_user=False)
        self.is_processing = False
        self.send_btn.configure(state="normal", text="Send ➤")
        self.status_label.configure(text="")
    
    def clear_chat(self):
        self.chat_frame.clear_messages()
        if self.agent:
            self.agent.clear_history()
        self.chat_frame.add_message(
            "🔄 Chat cleared! How can I help you?",
            is_user=False
        )


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
