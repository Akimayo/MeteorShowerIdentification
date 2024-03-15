namespace MeteorShowerIdentification.Rendering.Geometry;
internal readonly struct Projection
{

    private readonly Vector _camera;
    private readonly Rotation _angle;
    private readonly float[] _surface = new float[3];
    private readonly bool _isIdentity = false;

    public Projection(Vector camera)
    {
        _camera = camera;
        Vector cameraLookingAt = -camera.GetNormalized();
        _surface = [cameraLookingAt.X, cameraLookingAt.Y, cameraLookingAt.Z];
        if (camera.X == 0 && camera.Y == 0)
        {
            _isIdentity = true;
            return;
        }
        Vector cameraFlat = new(camera.X, camera.Y);
        _angle = new(
            0, // sin θx
            camera.Z / camera.Norm, // sin θy
            camera.Y / cameraFlat.Norm, // sin θz
            1, // cos θx
            cameraFlat.Norm / camera.Norm, // cos θy
            camera.X / cameraFlat.Norm // cos θz
        );
    }

    /// <summary>
    /// Performs a camera projection on a vector.
    /// </summary>
    /// <remarks>
    /// Source: <see href="https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula"/>
    /// </remarks>
    /// <param name="vector">Vector to be projected</param>
    /// <returns>A projected vector</returns>
    public readonly Vector Apply(Vector vector)
    {
        Vector v = vector - _camera;
        if (_isIdentity) return new(_surface[2] / v.Z * v.X + _surface[0], _surface[2] / v.Z * v.Y + _surface[1]);
        Vector r = _angle.Apply(v);
        return new(
            _surface[2] / r.Z * r.X + _surface[0],
            _surface[2] / r.Z * r.Y + _surface[1]
            );
    }
}

internal static class Projections
{
    internal static Vector Project(this Vector vector, Projection projection) =>
        projection.Apply(vector);
    internal static Bezier Project(this Bezier bezier, Projection projection) =>
        new(projection.Apply(bezier.Point1),
            projection.Apply(bezier.Point2),
            projection.Apply(bezier.Point3));
    internal static Ellipse Project(this Ellipse ellipse, Projection projection) =>
        new(projection.Apply(ellipse.StartPoint),
            ellipse.Segment1.Project(projection),
            ellipse.Segment2.Project(projection));
}
