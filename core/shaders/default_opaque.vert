// opengl version
#version 330 core

// set the location of the texcoord, normals and position
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

// push the uvs, normals and fragment position
out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

// uniforms for the camera
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

// main
void main() {
    // return uvs, fragpos and normals
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    // set the position relative to global(world) position and camera point of view
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}