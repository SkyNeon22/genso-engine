#version 330 core


uniform sampler2D tex;

in vec3 uvs;
out vec4 f_color;

void main() {
    vec4 texColor = vec4(texture(tex, vec2(uvs.x, uvs.y)).rgba);
    if (texColor.a < 0.01)
    {
        discard;
    };
    f_color = texColor;
}