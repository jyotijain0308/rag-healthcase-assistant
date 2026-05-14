export function sanitizeInput(input: string) {

    return input
        .trim()
        .replace(/\s+/g, " ")
        .slice(0, 1000);
}

export function validateHealthcareQuery(
    input: string
) {

    if (!input.trim()) {
        return "Question cannot be empty";
    }

    if (input.length < 3) {
        return "Question is too short";
    }

    if (input.length > 1000) {
        return "Question is too long";
    }

    return null;
}

const blockedPatterns = [

    /ignore previous instructions/i,

    /reveal system prompt/i,

    /bypass security/i,

    /generate malware/i,

    /make poison/i,

    /harm someone/i,

    /self-harm/i,

    /hack/i,

    /exploit/i,
];

export function detectDangerousPrompt(
    input: string
) {

    return blockedPatterns.some((pattern) =>
        pattern.test(input)
    );
}