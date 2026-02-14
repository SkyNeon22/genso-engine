// opengl version
#version 330 core

// note: do not touch 2dsurf.frag or 2dsurf.vert

// global uniform of the surface info
uniform sampler2D tex;

// uvs and fragment_color
in vec3 uvs;
out vec4 f_color;

void main() {
    // get the fragment color
    vec4 texColor = vec4(texture(tex, vec2(uvs.x, uvs.y)).rgba);
    // discard all pixels with 0 alpha value
    if (texColor.a < 0.01)
    {
        discard;
    };
    // return the fragment color
    f_color = texColor;
}