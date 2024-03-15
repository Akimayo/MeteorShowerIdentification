namespace MeteorShowerIdentification.Rendering.Geometry;
internal readonly struct Bezier
{
    private readonly Vector[] _points = new Vector[3];
    public readonly Vector Point1 => _points[0];
    public readonly Vector Point2 => _points[1];
    public readonly Vector Point3 => _points[2];
    public readonly Vector this[int i] => _points[i];
    public static Bezier operator +(Bezier a, Vector b) => new(a.Point1 + b, a.Point2 + b, a.Point3 + b);
    public static Bezier operator *(Bezier a, float n) => new(a.Point1 * n, a.Point2 * n, a.Point3 * n);

    public Bezier(Vector point1, Vector point2, Vector point3)
    {
        _points[0] = point1;
        _points[1] = point2;
        _points[2] = point3;
    }

    public override string ToString() => $"Bezier Curve (start) ~> {_points[0]} ~> {_points[1]} -> {_points[2]}";
}
