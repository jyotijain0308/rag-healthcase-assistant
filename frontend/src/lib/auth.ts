const TOKEN_KEY = "token";

export const auth = {
    getToken() {
        if (typeof window === "undefined") return null;
        return localStorage.getItem(TOKEN_KEY);
    },

    setToken(token: string) {
        if (typeof window === "undefined") return;
        localStorage.setItem(TOKEN_KEY, token);
    },

    logout() {
        if (typeof window === "undefined") return;
        localStorage.removeItem(TOKEN_KEY);

        // optional
        window.location.href = "/login";
    },

    getUser() {
        const token = this.getToken();
        if (!token) return null;

        try {
            return JSON.parse(atob(token.split(".")[1]));
        } catch {
            return null;
        }
    },
};