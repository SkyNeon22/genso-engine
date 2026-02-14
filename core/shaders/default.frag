// opengl version
#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

// get the color of the light and the light itself
vec4 getLight(vec4 color) {
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return vec4(color.r * (ambient.r + diffuse.r + specular.r), color.g * (ambient.g + diffuse.g + specular.g), color.b * (ambient.b + diffuse.b + specular.b), color.a);
}

// main
void main() {
    float gamma = 2.2;
    // vec3 color = texture(u_texture_0, uv_0).rgb;
    vec4 color = vec4(texture(u_texture_0, uv_0).rgba);
    color = pow(color, vec4(gamma));

    color = getLight(color);

    color = pow(color, 1 / vec4(gamma));

    if (color.a < 0.01)
    {
        discard;
    };

    fragColor = vec4(color);
}










