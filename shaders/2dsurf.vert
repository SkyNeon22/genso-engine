#version 330 core

in vec3 vert;
in vec3 texcoord;
out vec3 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 1.0); // vert = 3 arguments (x, y, z)
}