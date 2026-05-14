const PROMPT_INJECTION_PATTERNS = [

    /ignore previous instructions/i,

    /ignore all instructions/i,

    /reveal system prompt/i,

    /show hidden instructions/i,

    /act as/i,

    /pretend to be/i,

    /bypass restrictions/i,

    /disable safety/i,

    /jailbreak/i,

    /developer message/i
];

const HEALTHCARE_UNSAFE_PATTERNS = [

    /prescribe medication/i,

    /exact dosage/i,

    /replace my doctor/i,

    /diagnose me/i,

    /treatment without doctor/i,

    /self-medicate/i,

    /suicide/i,

    /harm myself/i
];

export function detectPromptInjection(
    input: string
) {

    return PROMPT_INJECTION_PATTERNS.some(
        (pattern) => pattern.test(input)
    );
}

export function detectUnsafeHealthcareQuery(
    input: string
) {

    return HEALTHCARE_UNSAFE_PATTERNS.some(
        (pattern) => pattern.test(input)
    );
}