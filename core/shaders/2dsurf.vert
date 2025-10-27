// opengl version
#version 330 core

// note: do not touch 2dsurf.frag or 2dsurf.vert

// get the vert and texcoordinates, push the uvs to the fragment shader
in vec3 vert;
in vec3 texcoord;
out vec3 uvs;

// main
void main() {
    // return uvs
    uvs = texcoord;
    // set the surface positon to 0.0 (you can change that in the pentabuff, but it can lead to unexpected results)
    gl_Position = vec4(vert, 1.0); // vert = 3 arguments (x, y, z)
}