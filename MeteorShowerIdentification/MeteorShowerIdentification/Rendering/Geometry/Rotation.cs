namespace MeteorShowerIdentification.Rendering.Geometry;
internal readonly struct Rotation
{
    private readonly float[] _angle = new float[6];

    public Rotation(float angleX, float angleY, float angleZ)
    {
        _angle[0] = (float)Math.Sin(angleX);
        _angle[1] = (float)Math.Sin(angleY);
        _angle[2] = (float)Math.Sin(angleZ);
        _angle[3] = (float)Math.Cos(angleX);
        _angle[4] = (float)Math.Cos(angleY);
        _angle[5] = (float)Math.Cos(angleZ);
    }
    public Rotation(float sx, float sy, float sz, float cx, float cy, float cz)
    {
        _angle[0] = sx;
        _angle[1] = sy;
        _angle[2] = sz;
        _angle[3] = cx;
        _angle[4] = cy;
        _angle[5] = cz;
    }

    /// <summary>
    /// Rotates a vector.
    /// </summary>
    /// <remarks>
    /// Source: <see href="https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula"/>
    /// </remarks>
    /// <param name="v">Vector to be rotated</param>
    /// <returns>A rotated vector</returns>
    public Vector Apply(Vector v)
    {
        return new(_angle[4] * (_angle[2] * v.Y + _angle[5] * v.X) - _angle[1] * v.Z,
                   _angle[0] * (_angle[4] * v.Z + _angle[1] * (_angle[2] * v.Y + _angle[5] * v.X)) + _angle[3] * (_angle[5] * v.Y - _angle[2] * v.X),
                   _angle[3] * (_angle[4] * v.Z + _angle[1] * (_angle[2] * v.Y + _angle[5] * v.X)) - _angle[0] * (_angle[5] * v.Y - _angle[2] * v.X));
    }
}

internal static class Rotations
{
    public static Vector Rotate(this Vector vector, Rotation rotation) =>
        rotation.Apply(vector);
    public static Bezier Rotate(this Bezier bezier, Rotation rotation) =>
        new(rotation.Apply(bezier.Point1),
            rotation.Apply(bezier.Point2),
            rotation.Apply(bezier.Point3));
    public static Ellipse Rotate(this Ellipse ellipse, Rotation rotation) =>
        new(rotation.Apply(ellipse.StartPoint),
            ellipse.Segment1.Rotate(rotation),
            ellipse.Segment2.Rotate(rotation));
}
