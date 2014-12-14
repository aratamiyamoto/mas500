// generate colorful particles moving and bouncing randomly in the
// window.

int randomInt(int min, int max) {
  return (int)floor(random(min, max + 1));
}

class Particle {
  final static int DEFAULT_TIME_TO_LIVE = 120;

  float mX;
  float mY;
  float mVX;
  float mVY;

  int mRadius;
  
  int mColorR;
  int mColorG;
  int mColorB;
  
  int mTimeToLive;
  
  public Particle(float x, float y, float vX, float vY, int radius) {
    mX = x;
    mY = y;
    mVX = vX;
    mVY = vY;
    
    mRadius = radius;
    
    mColorR = randomInt(0, 255);
    mColorG = randomInt(0, 255);
    mColorB = randomInt(0, 255);

    mTimeToLive = DEFAULT_TIME_TO_LIVE;
  }
  
  public void update() {
    mX += mVX;
    mY += mVY;
    
    bounce();
    
    if (mTimeToLive > 0) {
      --mTimeToLive;
    }
  }
  
  private void bounce() {
    if (mX + mRadius > width) {
      mX = width * 2 - (mX + mRadius * 2);
      mVX *= -1;
    }
    if (mX - mRadius < 0) {
      mX = mRadius * 2 - mX;
      mVX *= -1;
    }
    
    if (mY + mRadius > height) {
      mY = height * 2 - (mY + mRadius * 2);
      mVY *= -1;
    }
    if (mY - mRadius < 0) {
      mY = mRadius * 2 - mY;
      mVY *= -1;
    }
  }
  
  public boolean isAlive() {
    return mTimeToLive > 0;
  }
  
  public void render() {
    int alpha = mTimeToLive * 255 / DEFAULT_TIME_TO_LIVE;
    
    noStroke();
    fill(mColorR, mColorG, mColorB, alpha);
    ellipse((int)mX, (int)mY, (int)(mRadius * 2), (int)(mRadius * 2)); 
  }
}

class ParticleList {
  final static float MAX_SPEED = 5.0;
  final static int MIN_RADIUS = 10;
  final static int MAX_RADIUS = 25;
  final static int NUM_GENERATED_BALLS = 8;
  
  ArrayList<Particle> particles;
 
  public ParticleList() {
     particles = new ArrayList<Particle>();
  }
  
  public void addParticle(Particle particle) {
    particles.add(particle);
  }
  
  public void update() {
    for (int i = 0; i < particles.size(); i++) {
      particles.get(i).update();
    }
  }
  
  public void render() {
    for (int i = 0; i < particles.size(); i++) {
      particles.get(i).render();
    }
  }
  
  public void deleteDeadParticles() {
    for (int i = 0; i < particles.size();) {
      if (particles.get(i).isAlive()) {
        i++;
      } else {
        particles.remove(i);
      }
    }
  }
  
  public void generate(int x, int y) {
    for (int i = 0; i < NUM_GENERATED_BALLS; i++) {
      float vX = random(-MAX_SPEED, MAX_SPEED);
      float vY = random(-MAX_SPEED, MAX_SPEED);
      int radius = randomInt(MIN_RADIUS, MAX_RADIUS);
      
      Particle particle = new Particle(x, y, vX, vY, radius);
      this.addParticle(particle);
    }
  }
}

ParticleList particleList = new ParticleList();

void setup() {
  size(480, 480);
  
  particleList.generate(width / 2, height / 2);
  particleList.generate(width / 4, height / 4);
  particleList.generate(width * 3 / 4, height / 4);
  particleList.generate(width / 4, height * 3 / 4);
  particleList.generate(width * 3 / 4, height * 3 / 4);
}

void draw() {
  background(245, 245, 255);
  
  textFont(createFont("Arial", 24, true), 24);
  fill(0, 0, 90);
  text("Left-click in the window!", 10, 30);

  particleList.update();
  particleList.deleteDeadParticles();
  particleList.render();
}

void mousePressed() {
  particleList.generate(mouseX, mouseY);
}
