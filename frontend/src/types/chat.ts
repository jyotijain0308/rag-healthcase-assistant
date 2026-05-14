export interface Source {
    page: number;
    source: string;
    filename: string;
    preview: string;
    score: number;
}

export interface ChatPart {
    type: string;
    text: string;
}

export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    parts: ChatPart[];
    sources?: Source[];
}