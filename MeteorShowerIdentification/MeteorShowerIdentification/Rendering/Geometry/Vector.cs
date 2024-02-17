namespace MeteorShowerIdentification.Rendering.Geometry;
internal struct Vector
{
    public static Vector Origin => new();
    private readonly float[] _pos = [0, 0, 0];
    public readonly float X { get => _pos[0]; set { _pos[0] = value; } }
    public readonly float Y { get => _pos[1]; set { _pos[1] = value; } }
    public readonly float Z { get => _pos[2]; set { _pos[2] = value; } }
    public readonly float this[int axis]
    {
        get => _pos[axis];
        set { _pos[axis] = value; }
    }
    public static Vector operator -(Vector a) => new(-a.X, -a.Y, -a.Z);
    public static Vector operator -(Vector a, Vector b) => new(a.X - b.X, a.Y - b.Y, a.Z - b.Z);
    public static Vector operator +(Vector a, Vector b) => new(a.X + b.X, a.Y + b.Y, a.Z + b.Z);
    public static Vector operator /(Vector a, float n) => new(a.X / n, a.Y / n, a.Z / n);
    public static Vector operator *(Vector a, float n) => new(a.X * n, a.Y * n, a.Z * n);

    private bool _hasNormSq = false, _hasNorm = false;
    private float _normSq, _norm;
    public float NormSq { get { if (!_hasNormSq) { _normSq = _pos[0] * _pos[0] + _pos[1] * _pos[1] + _pos[2] * _pos[2]; _hasNormSq = true; } return _normSq; } }
    public float Norm { get { if (!_hasNorm) { _norm = (float)Math.Sqrt(NormSq); _hasNorm = true; } return _norm; } }

    public Vector() { }
    public Vector(float x, float y)
    {
        _pos[0] = x;
        _pos[1] = y;
    }
    public Vector(float x, float y, float z)
    {
        _pos[0] = x;
        _pos[1] = y;
        _pos[2] = z;
    }

    public Vector GetNormalized() => this / Norm;

    public override readonly string ToString() => $"({_pos[0]}, {_pos[1]}, {_pos[2]})";
}
